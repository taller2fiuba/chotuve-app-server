from flask_restful import Resource
from flask import request, g
import requests
from app import app
from app.login_requerido_decorator import login_requerido

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class Video(Resource):
    @login_requerido
    def post(self):
        usuario_id = g.usuario_actual

        body = request.get_json(force=True)
        url = body['url']
        titulo = body['titulo']

        datos = {"url": url, "titulo": titulo, "usuario_id": usuario_id}
        response = requests.post(
            CHOTUVE_MEDIA_URL + "/video", json=datos)

        return response.json(), response.status_code
