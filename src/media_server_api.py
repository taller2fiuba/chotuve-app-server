import requests
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

RUTA_VIDEO = '/video'

def post_to_media_server(ruta, datos):
    return requests.post(CHOTUVE_MEDIA_URL + ruta, json=datos)


def get_to_media_server(ruta, params):
    return requests.get(CHOTUVE_MEDIA_URL + ruta, params=params)

def subir_video(datos):
    return post_to_media_server(RUTA_VIDEO, datos)

def get_videos(params):
    return get_to_media_server(RUTA_VIDEO, params)

def limpiar_base_de_datos():
    return requests.delete(f'{CHOTUVE_MEDIA_URL}/base_de_datos')
