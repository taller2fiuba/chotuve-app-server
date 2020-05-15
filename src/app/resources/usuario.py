from flask_restful import Resource
from flask import request
import requests
from config import Config

CHOTUVE_AUTH_URL = Config.CHOTUVE_AUTH_URL

class Usuario(Resource):
    def post(self):
        body = request.get_json(force=True)
        mail = body['mail']
        contra = body['contraseña']

        response = requests.post(
            CHOTUVE_AUTH_URL + "/usuario", json={"mail": mail, "contraseña": contra})

        return response.json(), response.status_code
