from flask import request, g, abort

from app.login_requerido_decorator import login_requerido
from app.recursos.video.video_base import VideoBaseResource
from app.models.contacto import Contacto
from app.servicios import auth_server, media_server

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10

class VideoUsuarioResource(VideoBaseResource):
    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual
        else:
            # verificar que exista el usuario
            if not auth_server.obtener_usuario(usuario_id):
                return {}, 404

        offset = request.args.get('offset', str(OFFSET_POR_DEFECTO))
        cantidad = request.args.get('cantidad', str(CANTIDAD_POR_DEFECTO))

        if not offset.isdigit() or not cantidad.isdigit():
            abort(400)

        con_privados = usuario_id == g.usuario_actual or \
                       Contacto.es_contacto(usuario_id, g.usuario_actual)

        videos = media_server.obtener_videos_usuario(usuario_id,
                                                     con_privados,
                                                     offset=int(offset),
                                                     cantidad=int(cantidad))

        return [self.armar_video_sin_autor(v) for v in videos], 200
