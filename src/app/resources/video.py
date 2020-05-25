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
        url = post_data.get('url', '')
        titulo = post_data.get('titulo', '')
        descripcion = post_data.get('descripcion', '')
        ubicacion = post_data.get('ubicacion', '')
        visibilidad = post_data.get('visibilidad', '')
        usuario_id = g.usuario_actual

        datos = {
            'url': url,
            'titulo': titulo,
            'descripcion': descripcion,
            'ubicacion': ubicacion,
            'visibilidad': visibilidad,
            'usuario_id': usuario_id,
        }

        response = media_server_api.subir_video(datos)

        return response.json(), response.status_code
