import requests
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

def post_to_media_server(ruta, datos):
    response = requests.post(CHOTUVE_MEDIA_URL + ruta, json=datos)

    return response

def get_to_media_server(ruta, params):
    response = requests.get(CHOTUVE_MEDIA_URL + ruta, params=params)

    return response

def subir_video(datos):
    ruta = "/video"

    return post_to_media_server(ruta, datos)

def get_videos(params):
    ruta = "/video"

    return get_to_media_server(ruta, params)
