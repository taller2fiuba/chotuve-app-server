from flask_restful import Resource
from flask import request, g

from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server

class UsuarioResource(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']

        data = auth_server.registrar_usuario(email, password)
        if not data:
            return {'errores': {'email': 'El mail ya se encuentra registrado'}}, 400

        token, uid = data
        return {'auth_token': token, 'id': uid}, 201

    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual

        data = auth_server.obtener_usuario(usuario_id)
        if not data:
            return {}, 404

        return data, 200
