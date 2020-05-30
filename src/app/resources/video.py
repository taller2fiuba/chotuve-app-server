from flask_restful import Resource
from flask import request, g
from app import app
from app.login_requerido_decorator import login_requerido
import media_server_api
import auth_server_api

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

        ids = ','.join([str(video['usuario_id']) for video in videos])
        params = {'ids': ids, 'offset': offset, 'cantidad': cantidad}
        response = auth_server_api.get_usuarios(params)
        usuarios = response.json()

        for i, video in enumerate(videos):
            # TODO ver si se puede mejorar
            usuario = [usuario for usuario in usuarios if usuario['id'] == video['usuario_id']][0]
            videos[i] = self._armar_video(video, usuario)

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

    def _armar_video(self, video, usuario):
        return {
            'id': video['_id'],
            'url': video['url'],
            'titulo': video['titulo'],
            'duracion': video['duracion'],
            'creacion': video['time_stamp'],
            'visibilidad': video['visibilidad'],
            'autor': {
                'usuario_id': usuario['id'],
                'nombre': usuario['nombre'],
                'apellido': usuario['apellido']
                }
        }
