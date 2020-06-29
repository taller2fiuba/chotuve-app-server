from flask_restful import Resource
from flask import request, g
import auth_server_api
from app.login_requerido_decorator import login_requerido

class UsuarioResource(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']

        response = auth_server_api.registro_nuevo_usuario(email, password)

        return response.json(), response.status_code

    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual

        response = auth_server_api.get_usuario(usuario_id)

        return response.json(), response.status_code
