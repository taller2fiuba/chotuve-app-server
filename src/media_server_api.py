import requests
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

def post_to_media_server(ruta, datos):
    response = requests.post(
        CHOTUVE_MEDIA_URL + ruta, json=datos)
    return response

def subir_video(datos):
    ruta = "/video"

    return post_to_media_server(ruta, datos)
