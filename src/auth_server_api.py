import requests

from flask import g

from app import app

CHOTUVE_AUTH_URL = app.config.get('CHOTUVE_AUTH_URL')

def post_to_auth_server(ruta, datos):
    response = requests.post(
        CHOTUVE_AUTH_URL + ruta, json=datos)
    return response

def put_to_auth_server(ruta, datos):
    response = requests.put(
        CHOTUVE_AUTH_URL + ruta, json=datos)
    return response

def get_to_auth_server(ruta, datos):
    response = requests.get(
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

def limpiar_base_de_datos():
    return requests.delete(f'{CHOTUVE_AUTH_URL}/base_de_datos')

def autentificar(headers):
    return requests.get(f'{CHOTUVE_AUTH_URL}/usuario/sesion', headers=headers)

def get_usuario(usuario_id):
    return requests.get(f'{CHOTUVE_AUTH_URL}/usuario/{int(usuario_id)}')

def actualizar_perfil_usuario(nombre, apellido, telefono, direccion):
    datos = {"nombre": nombre, "apellido": apellido, "telefono": telefono, "direccion": direccion}
    ruta = "/usuario/"+str(g.usuario_actual)

    return put_to_auth_server(ruta, datos)

def get_perfil(id_usuario):
    ruta = "/usuario/"+str(id_usuario)

    return get_to_auth_server(ruta, {})

def obtener_usuarios(params):
    return requests.get(f'{CHOTUVE_AUTH_URL}/usuario', params=params)
