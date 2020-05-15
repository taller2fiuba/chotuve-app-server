import requests
from config import Config

CHOTUVE_AUTH_URL = Config.CHOTUVE_AUTH_URL


def post_to_auth_server(ruta, datos):
    response = requests.post(
        CHOTUVE_AUTH_URL + ruta, json=datos)
    return response

def iniciar_sesion(mail, contra):
    datos = {"mail": mail, "contraseña": contra}
    ruta = "/usuario/sesion"

    response = post_to_auth_server(ruta, datos)

    return response

def registro_nuevo_usuario(mail, contra):
    datos = {"mail": mail, "contraseña": contra}
    ruta = "/usuario"

    response = post_to_auth_server(ruta, datos)

    return response
