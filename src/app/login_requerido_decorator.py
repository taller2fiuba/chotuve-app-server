from functools import wraps
from flask import request

import auth_server_api
from app.repositorios import usuario_actual_repositorio

def login_requerido(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        respuesta = auth_server_api.autentificar(request.headers)
        if respuesta.status_code == 200:
            usuario_actual_repositorio.set_usuario_actual(respuesta.json()['usuario_id'])
            return funcion(*args, **kwargs)
        return {}, respuesta.status_code
    return decorated_function
