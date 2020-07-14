import requests

class ClienteHttpBase:
    def __init__(self, url: str, app_token=None):
        '''
        url: URL del servidor de autenticación
        '''
        self._url = url.rstrip('/')
        self._app_token = app_token

    def _get(self, path: str, params=None, headers=None):
        '''
        Realiza una solicitud GET al servidor de autenticación.
        '''
        return self._do_http_request(requests.get, path, params=params, headers=headers)

    def _post(self, path: str, json: dict, params=None, headers=None):
        '''
        Realiza una solicitud POST al servidor de autenticación.
        '''
        return self._do_http_request(requests.post, path, json=json, params=params, headers=headers)

    def _put(self, path: str, json: dict, params=None, headers=None):
        '''
        Realiza una solicitud PUT al servidor de autenticación.
        '''
        return self._do_http_request(requests.put, path, json=json, params=params, headers=headers)

    def _delete(self, path: str, json=None, params=None, headers=None):
        '''
        Realiza una solicitud PUT al servidor de autenticación.
        '''
        return self._do_http_request(requests.delete, path, json=json, params=params,
                                     headers=headers)

    # pylint: disable=too-many-arguments
    def _do_http_request(self, method, path: str, json=None, params=None, headers=None):
        '''
        Realiza una solicitud al servidor de autenticación utilizado el método pasado por parámetro.
        method: requests.get, requests.post o requests.put
        '''
        extra_headers = {'X-APP-SERVER-TOKEN': self._app_token}
        extra_headers.update(headers or {})

        return method(f"{self._url}{path}", params=params, headers=extra_headers, json=json)
