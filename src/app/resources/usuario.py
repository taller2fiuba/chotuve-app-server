from flask_restful import Resource
from flask import request
import auth_server_api

class Usuario(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']

        response = auth_server_api.registro_nuevo_usuario(email, password)

        return response.json(), response.status_code
