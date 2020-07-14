from functools import wraps
from flask import request

from app.servicios import auth_server
from app.repositorios import usuario_actual_repositorio

def login_requerido(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '')[len('Bearer '):]
        usuario_id = auth_server.autenticar(token)
        if not usuario_id:
            return {}, 401
        usuario_actual_repositorio.set_usuario_actual(usuario_id)
        return funcion(*args, **kwargs)
    return decorated_function
