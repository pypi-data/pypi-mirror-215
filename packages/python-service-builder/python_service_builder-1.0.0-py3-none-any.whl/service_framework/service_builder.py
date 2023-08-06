# Copyright 2022 David Harcombe. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Service Builder Class.

Authenticate and fetch a discoverable API service.
"""
from __future__ import annotations

import dataclasses
import logging
from typing import Any, List, Mapping, Optional, Union

import dataclasses_json
import google_auth_httplib2
from apiclient import discovery
from google.auth import exceptions
from google.oauth2 import credentials as oauth
from httplib2 import Http
from oauth2client import service_account

from service_framework.services import Service
from service_framework import snake_field


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class OAuthKey(object):
  """Dataclass from the json key.

  NOTE: This is by no means the entire key; just the fields neccessary for OAuth.
  """
  access_token: Optional[str] = snake_field(field_name='token')
  refresh_token: Optional[str] = snake_field()
  token_uri: Optional[str] = snake_field()
  client_id: Optional[str] = snake_field()
  client_secret: Optional[str] = snake_field()


def build_service(service: Service,
                  key: Union[OAuthKey, oauth.Credentials,
                             str, Mapping[str, str]],
                  api_key: Optional[str] = None,
                  extra_scopes: Optional[List[str]] = None) -> discovery.Resource:
  """Fetches a discoverable API service.

  Args:
      service (Service): the service requested
      key (Union[OAuthKey, oauth.Credentials, str, Mapping[str, str]]):
        the user credentials/parameters
      api_key (Optional[str], optional): the API key for the service if needed. Defaults to None.
      extra_scopes (Optional[List[str]], optional): any extra OAuth scopes required. Defaults to None.

  Raises:
      Exception: any errors found during the creation process

  Returns:
      discovery.Resource: a service for REST calls
  """
  credentials = None
  definition = service.definition

  if isinstance(key, OAuthKey):
    kwargs = key.to_dict()
    if extra_scopes:
      kwargs['scopes'] = extra_scopes

    try:
      credentials = oauth.Credentials(**kwargs)
      https = google_auth_httplib2.AuthorizedHttp(credentials)

    except KeyError:
      logging.exception(
          'Invalid credentials received: missing a part of the credentials')
      raise

    except exceptions.RefreshError as error:
      logging.exception('Invalid credentials received')
      raise

  elif isinstance(key, oauth.Credentials):
    credentials = key
    https = google_auth_httplib2.AuthorizedHttp(credentials)

  elif isinstance(key, str):
    kwargs = {
        'filename': key,
    }
    if extra_scopes:
      kwargs['scopes'] = extra_scopes

    credentials = \
        service_account.ServiceAccountCredentials.from_json_keyfile_name(
            **kwargs)
    https = credentials.authorize(Http())

  elif isinstance(key, Mapping):
    kwargs = {
        'keyfile_dict': key,
    }

    if extra_scopes:
      kwargs['scopes'] = extra_scopes

    credentials = \
        service_account.ServiceAccountCredentials.from_json_keyfile_dict(
            key, scopes=extra_scopes)
    https = credentials.authorize(Http())

  else:
    raise Exception('No valid credentials provided.')

  discovery_args = {
      'http': https,
      'developerKey': api_key,
      'cache_discovery': False,
      **definition.to_dict()
  }

  return discovery.build(**discovery_args)
