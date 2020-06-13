from functools import wraps
from flask import request

import auth_server_api
from app.repositorios import usuario_actual_repositorio
from app import log

def login_requerido(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        log.info('Verificando login')
        respuesta = auth_server_api.autentificar(request.headers)
        log.info('Respuesta obtenida desde el auth server')
        if respuesta.status_code == 200:
            log.info('Autenticación correcta')
            usuario_actual_repositorio.set_usuario_actual(respuesta.json()['usuario_id'])
            return funcion(*args, **kwargs)
        log.info(f'Autenticación errónea, {respuesta.status_code}')
        return {}, respuesta.status_code
    return decorated_function
