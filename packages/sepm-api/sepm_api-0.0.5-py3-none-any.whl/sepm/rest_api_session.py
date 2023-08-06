from datetime import datetime
import json
import platform
import random
import sys
import time
import urllib.parse

import requests

from sepm.config import *
from sepm.exceptions import *
from sepm.__init__ import __version__

# main module interface
class RestApiSession(object):
    def __init__(
        self,
        logger,
        username,
        password,
        domain,
        base_url=DEFAULT_BASE_URL,
        auth_url=AUTH_URL,
        simulate=SIMULATE_API,
        retry_4xx_error=RETRY_4XX_ERROR,
        retry_4xx_error_wait_time=RETRY_4XX_ERROR_WAIT_TIME,
        maximum_retries=MAXIMUM_RETRIES,
    ):
        super(RestApiSession, self).__init__()

        # initialize attributes and properties
        self._version = __version__
        self._username = username
        self._password = password
        self._domain = domain
        self._api_key = "CHANGEME" # this will be updated on authn success
        self._base_url = str(base_url)
        self._auth_url = str(auth_url)
        self._simulate = simulate
        self._retry_4xx_error = retry_4xx_error
        self._retry_4xx_error_wait_time = retry_4xx_error_wait_time
        self._maximum_retries = maximum_retries

        #create payload for authentication
        payload = {
            "username": self._username,
            "password": self._password,
            "domain": self._domain
        }

        auth_req = requests.post(self._auth_url,
                    headers= {"Content-Type": "application/json"},
                    data=json.dumps(payload))

        isAuthenticated = False
        if auth_req.status_code == 200:
            isAuthenticated = True

        if isAuthenticated:
            self._api_key = auth_req.json()["token"]

        # initialize a new `requests` session
        self._req_session = requests.session()
        self._req_session.encoding = 'utf-8'

        # Update the headers for the session
        self._req_session.headers = {
            'Authorization': 'Bearer ' + self._api_key,
            'Content-Type': 'application/json',
        }

        # Log API calls
        self._logger = logger
        self._parameters = {'version': self._version}
        self._parameters.update(locals())
        self._parameters.pop('self')
        self._parameters.pop('logger')
        self._parameters.pop('__class__')
        self._parameters['api_key'] = '*' * 36 + self._api_key[-4:]
        if self._logger:
            self._logger.info(f'Symantec Endpoint Protection Manager API session initialized with these parameters: {self._parameters}')

    def request(self, metadata, method, url, **kwargs):
        # Metadata on endpoint
        tag = metadata['tags'][0]
        operation = metadata['operation']

        abs_url = self._base_url + url

        # Set maximum number of retries
        retries = self._maximum_retries

        # simulate non-safe API calls without actually sending them
        if self._logger:
            self._logger.debug(metadata)
        if self._simulate and method != 'GET':
            if self._logger:
                self._logger.info(f'{tag}, {operation}, {method} - {abs_url} - SIMULATED')
            return None
        else:
            response = None
            while retries > 0:
                # Make the HTTP request to the API endpoint
                try:
                    if response:
                        response.close()
                    if self._logger:
                        self._logger.info(f'{method} {abs_url}')
                    response = self._req_session.request(method, abs_url, allow_redirects=False, **kwargs)
                    reason = response.reason if response.reason else ''
                    status = response.status_code
                except requests.exceptions.RequestException as e:
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                    time.sleep(1)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)
                    else:
                        continue
                # TODO: not all endpoints return response as json
                # 2XX success
                if response.ok:
                    if self._logger:
                        self._logger.info(f'{tag}, {operation} - {status} {reason}')

                    ret = None
                    try:
                        if method == 'GET' and response.content.strip():
                            ret = response.json()
                        return response
                    except json.decoder.JSONDecodeError as e:
                        if self._logger:
                            self._logger.warning(f'{tag}, {operation} - {e}, retrying in 1 second')
                        time.sleep(1)
                        retries -= 1
                        if retries == 0:
                            raise APIError(metadata, response)
                        else:
                            continue

                # 5XX errors
                elif status >= 500:
                    if self._logger:
                        self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in 1 second')
                    time.sleep(1)
                    retries -= 1
                    if retries == 0:
                        raise APIError(metadata, response)

                # 4XX errors
                else:
                    try:
                        message = response.json()
                    except ValueError:
                        message = response.content[:100]

                    if self._retry_4xx_error:
                        wait = random.randint(1, self._retry_4xx_error_wait_time)
                        if self._logger:
                            self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in {wait} seconds')
                        time.sleep(wait)
                        retries -= 1
                        if retries == 0:
                            raise APIError(metadata, response)

                    # All other client-side errors
                    else:
                        if self._logger:
                            self._logger.error(f'{tag}, {operation} - {status} {reason}, {message}')
                        raise APIError(metadata, response)

    def get(self, metadata, url, params=None):
        metadata['method'] = 'GET'
        metadata['url'] = url
        metadata['params'] = params
        response = self.request(metadata, 'GET', url, params=params)

        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def post(self, metadata, url, json=None):
        metadata['method'] = 'POST'
        metadata['url'] = url
        metadata['json'] = json
        response = self.request(metadata, 'POST', url, json=json)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def put(self, metadata, url, json=None):
        metadata['method'] = 'PUT'
        metadata['url'] = url
        metadata['json'] = json
        response = self.request(metadata, 'PUT', url, json=json)
        ret = None
        if response:
            if response.content.strip():
                ret = response.json()
            response.close()
        return ret

    def delete(self, metadata, url, json=None):
        metadata['method'] = 'DELETE'
        metadata['url'] = url
        response = self.request(metadata, 'DELETE', url, json=json)
        if response:
            response.close()
        return None