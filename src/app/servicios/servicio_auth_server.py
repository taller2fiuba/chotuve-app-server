import requests

class AuthServerError(Exception):
    def __init__(self, response):
        super().__init__()
        self.status_code = response.status_code
        self.payload = response.json()

class AuthServer:
    def __init__(self, url: str):
        '''
        url: URL del servidor de autenticación
        '''
        self._url = url.rstrip('/')

    def obtener_usuario(self, usuario_id: int):
        '''
        Devuelve un diccionario con la información del usuario
        o None si el usuario no existe.
        '''
        response = requests.get(f'{self._url}/usuario/{usuario_id}')
        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise AuthServerError(response)

        return response.json()
