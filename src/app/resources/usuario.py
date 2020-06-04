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

class PerfilUsuarioResource(Resource):

    @login_requerido
    def get(self):
        response = auth_server_api.get_perfil(g.usuario_actual)

        return response.json(), response.status_code

    @login_requerido
    def put(self):
        campos_requeridos = ('nombre', 'apellido')
        campos = ('nombre', 'apellido', 'telefono', 'direccion')
        post_data = request.get_json()
        if not post_data: #no hay body
            return {}, 400
        if not all(parametros in post_data for parametros in campos_requeridos):
            return {}, 400

        for campo in campos:
            if campo not in post_data:
                post_data[campo] = None

        nombre = post_data['nombre']
        apellido = post_data['apellido']
        telefono = post_data['telefono']
        direccion = post_data['direccion']

        response = auth_server_api.actualizar_perfil_usuario(nombre, apellido, telefono, direccion)

        return response.json(), response.status_code

class PerfilOtroUsuarioResource(Resource):

    @login_requerido
    def get(self, usuario_id):
        response = auth_server_api.get_perfil(usuario_id)

        return response.json(), response.status_code
