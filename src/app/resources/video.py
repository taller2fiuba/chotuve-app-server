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
        datos = self._obtener_datos(post_data)

        response = media_server_api.subir_video(datos)

        return response.json(), response.status_code

    @login_requerido
    def get(self):
        offset = int(request.args.get('offset', 0))
        cantidad = int(request.args.get('cantidad', 10))
        params = {'offset': offset, 'cantidad': cantidad}

        response = media_server_api.get_videos(params)
        videos = response.json()

        for i, video in enumerate(videos):
            videos[i] = self._armar_video(video)

        return videos, response.status_code

    def _obtener_datos(self, post_data):
        return {
            'url': post_data.get('url', None),
            'titulo': post_data.get('titulo', None),
            'descripcion': post_data.get('descripcion', None),
            'ubicacion': post_data.get('ubicacion', None),
            'duracion': post_data.get('duracion', 0),
            'usuario_id': g.usuario_actual,
            'visibilidad': post_data.get('visibilidad', 'publico'),
        }

    def _armar_video(self, video):
        return {
            'id': video['_id'],
            'url': video['url'],
            'titulo': video['titulo'],
            'duracion': video['duracion'],
            'creacion': video['time_stamp'],
            'visibilidad': video['visibilidad'],
            'author': {'usuario_id': video['usuario_id']} # llamar al auth_server
        }
