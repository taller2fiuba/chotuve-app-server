from flask_restful import Resource
from flask import request, g

from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server

class UsuarioClaveResource(Resource):
    @login_requerido
    def put(self):
        post_data = request.get_json()
        nueva_password = post_data['password']

        if not auth_server.actualizar_clave(g.usuario_actual, nueva_password):
            return {'mensaje': 'La nueva clave es inválida.'}, 400

        return {}, 200
