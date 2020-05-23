import requests
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

def post_to_media_server(ruta, datos):
    response = requests.post(
        CHOTUVE_MEDIA_URL + ruta, json=datos)
    return response

def subir_video(url, titulo, usuario_id):
    datos = {"url": url, "titulo": titulo, "usuario_id": usuario_id}
    ruta = "/video"

    return post_to_media_server(ruta, datos)
