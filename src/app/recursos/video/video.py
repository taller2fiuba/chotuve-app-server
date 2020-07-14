from flask import request, g
from app import app
from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server
import media_server_api
from .video_base import VideoBaseResource


CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')
OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10
DURACION_POR_DEFECTO = 0

class VideoResource(VideoBaseResource):
    @login_requerido
    def post(self):
        post_data = request.get_json(force=True)
        datos = self._obtener_datos(post_data)

        response = media_server_api.subir_video(datos)

        return response.json(), response.status_code

    @login_requerido
    def get(self):
        offset = int(request.args.get('offset', OFFSET_POR_DEFECTO))
        cantidad = int(request.args.get('cantidad', CANTIDAD_POR_DEFECTO))
        params = {'offset': offset, 'cantidad': cantidad}
        response = media_server_api.obtener_videos(params)
        if response.status_code != 200:
            return response.json(), response.status_code

        # remover los videos del usuario actual
        videos = response.json()
        videos = list(filter(lambda video: (video['usuario_id'] != g.usuario_actual), videos))
        if not videos:
            return [], 200

        autores = auth_server.obtener_usuarios({v['usuario_id'] for v in videos})

        for i, video in enumerate(videos):
            videos[i] = self.armar_video(video, autores[video['usuario_id']])

        return videos, 200

    def _obtener_datos(self, post_data):
        return {
            'url': post_data.get('url', None),
            'titulo': post_data.get('titulo', None),
            'descripcion': post_data.get('descripcion', None),
            'ubicacion': post_data.get('ubicacion', None),
            'duracion': post_data.get('duracion', DURACION_POR_DEFECTO),
            'usuario_id': g.usuario_actual,
            'visibilidad': post_data.get('visibilidad', 'publico')
        }

    def _obtener_autores(self, videos, offset, cantidad):
        ids = ','.join({str(video['usuario_id']) for video in videos})
        params = {'ids': ids, 'offset': offset, 'cantidad': cantidad}

        return auth_server.obtener_usuarios(params)
