from flask_restful import Resource
from flask import request
import auth_server_api

class Sesion(Resource):
    def post(self):
        body = request.get_json(force=True)
        mail = body['mail']
        contra = body['contraseña']

        response = auth_server_api.iniciar_sesion(mail, contra)

        return response.json(), response.status_code
