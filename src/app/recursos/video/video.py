from flask import request, g, abort

from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server, media_server
from app.models.contacto import Contacto

from .video_base import VideoBaseResource

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10
DURACION_POR_DEFECTO = 0

class VideoResource(VideoBaseResource):
    @login_requerido
    def post(self):
        post_data = request.get_json(force=True)
        data_video = {
            'url': post_data.get('url', None),
            'titulo': post_data.get('titulo', None),
            'descripcion': post_data.get('descripcion', None),
            'ubicacion': post_data.get('ubicacion', None),
            'duracion': post_data.get('duracion', DURACION_POR_DEFECTO),
            'usuario_id': g.usuario_actual,
            'visibilidad': post_data.get('visibilidad', 'publico')
        }

        if not media_server.subir_video(data_video):
            return {}, 400

        return {}, 201

    @login_requerido
    def get(self):
        offset = request.args.get('offset', str(OFFSET_POR_DEFECTO))
        cantidad = request.args.get('cantidad', str(CANTIDAD_POR_DEFECTO))
        if not offset.isdigit() or not cantidad.isdigit():
            abort(400)

        contactos = Contacto.obtener_contactos(g.usuario_actual)
        videos = media_server.obtener_videos(contactos=contactos,
                                             offset=int(offset),
                                             cantidad=int(cantidad))

        videos = [v for v in videos if v['usuario_id'] != g.usuario_actual]
        if len(videos) > 0:
            autores = auth_server.obtener_usuarios({v['usuario_id'] for v in videos})

        for i, video in enumerate(videos):
            videos[i] = self.armar_video(video, autores[video['usuario_id']])

        return videos, 200
