from flask_restful import Resource
from flask import request

from app.servicios import auth_server

class Sesion(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']

        data = auth_server.iniciar_sesion(email, password)
        if not data:
            return {'mensaje': 'Email o constraseña invalidos'}, 400

        token, uid = data
        return {'auth_token': token, 'id': uid}, 200
