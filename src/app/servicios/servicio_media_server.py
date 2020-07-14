import requests

class MediaServerError(Exception):
    def __init__(self, response):
        super().__init__()
        self.status_code = response.status_code
        self.payload = response.json()

class MediaServer:
    def __init__(self, url: str):
        '''
        url: URL del servidor de medios
        '''
        self._url = url.rstrip('/')

    def obtener_video(self, video_id: str):
        '''
        Obtiene la información de un video.
        Devuelve un diccionario con toda la información del video, o None si
        no hay un video con ese ID.
        '''
        response = requests.get(f"{self._url}/video/{video_id}")
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            return None

        raise MediaServerError(response)

    def obtener_videos(self, offset=0, cantidad=10):
        '''
        Obtiene videos desde el media server.
        offset: Ignorar tantos videos como este parámetro indique.
        cantidad: Obtener, como máximo, tantos videos como este parámetro indique.

        Devuelve un iterable donde cada elemento es un diccionario con la
        información del video.
        '''
        response = requests.get(f"{self._url}/video", params={
            'cantidad': cantidad,
            'offset': offset
        })

        if response.status_code != 200:
            raise MediaServerError(response)

        return response.json()

    def subir_video(self, data: dict):
        '''
        Sube un nuevo video al servidor de medios.

        data: Diccionario con toda la información del video a subir.
        '''
        response = requests.post(f"{self._url}/video", json=data)

        if response.status_code != 201:
            raise MediaServerError(response)

    def limpiar_base_de_datos(self):
        '''
        Borra la base de datos del servidor de medios.

        Devuelve True si se borró correctamente, False en caso contrario.
        '''
        response = requests.delete(f'{self._url}/base_de_datos')
        return response.status_code == 200
