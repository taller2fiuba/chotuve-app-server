import requests
from config import Config

CHOTUVE_AUTH_URL = Config.CHOTUVE_AUTH_URL


def post_to_auth_server(ruta, datos):
    response = requests.post(
        CHOTUVE_AUTH_URL + ruta, json=datos)
    return response

def iniciar_sesion(email, password):
    datos = {"email": email, "password": password}
    ruta = "/usuario/sesion"

    return post_to_auth_server(ruta, datos)

def registro_nuevo_usuario(email, password):
    datos = {"email": email, "password": password}
    ruta = "/usuario"

    return post_to_auth_server(ruta, datos)
