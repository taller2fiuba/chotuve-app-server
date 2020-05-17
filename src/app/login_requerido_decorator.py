from functools import wraps
from flask import g, request

import auth_server_api

def login_requerido(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        respuesta = auth_server_api.autentificar(request.headers)
        if respuesta.status_code == 200:
            g.usuario_actual = respuesta.json()['usuario_id']
            return funcion(*args, **kwargs)
        return {}, respuesta.status_code
    return decorated_function
