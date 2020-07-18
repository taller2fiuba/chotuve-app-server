from functools import wraps
from flask import request

from app.servicios import auth_server
from app.repositorios import usuario_actual_repositorio

def login_requerido(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '')[len('Bearer '):]
        data = auth_server.autenticar(token)
        if not data:
            return {}, 401
        usuario_id, es_admin = data
        usuario_actual_repositorio.set_usuario_actual(usuario_id, es_admin)
        return funcion(*args, **kwargs)
    return decorated_function
