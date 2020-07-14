from flask import request, g

from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server, media_server

from .video_base import VideoBaseResource

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10
DURACION_POR_DEFECTO = 0

class VideoResource(VideoBaseResource):
    @login_requerido
    def post(self):
        post_data = request.get_json(force=True)

        media_server.subir_video({
            'url': post_data.get('url', None),
            'titulo': post_data.get('titulo', None),
            'descripcion': post_data.get('descripcion', None),
            'ubicacion': post_data.get('ubicacion', None),
            'duracion': post_data.get('duracion', DURACION_POR_DEFECTO),
            'usuario_id': g.usuario_actual,
            'visibilidad': post_data.get('visibilidad', 'publico')
        })

        return {}, 201

    @login_requerido
    def get(self):
        offset = int(request.args.get('offset', OFFSET_POR_DEFECTO))
        cantidad = int(request.args.get('cantidad', CANTIDAD_POR_DEFECTO))
        videos = media_server.obtener_videos(offset=offset, cantidad=cantidad)

        # remover los videos del usuario actual
        videos = [v for v in videos if v['usuario_id'] != g.usuario_actual]
        if not videos:
            return [], 200

        autores = auth_server.obtener_usuarios({v['usuario_id'] for v in videos})

        for i, video in enumerate(videos):
            videos[i] = self.armar_video(video, autores[video['usuario_id']])

        return videos, 200
