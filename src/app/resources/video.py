from flask_restful import Resource
from flask import request, g
from app import app
from app.login_requerido_decorator import login_requerido
import media_server_api

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class Video(Resource):
    @login_requerido
    def post(self):
        post_data = request.get_json(force=True)
        url = post_data['url']
        titulo = post_data['titulo']
        usuario_id = g.usuario_actual

        response = media_server_api.subir_video(url, titulo, usuario_id)

        return response.json(), response.status_code
