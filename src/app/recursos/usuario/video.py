from flask import request, g, abort
import media_server_api
import auth_server_api
from app.login_requerido_decorator import login_requerido
from app.recursos.video.video_base import VideoBaseResource

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10

class VideoUsuarioResource(VideoBaseResource):
    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual
        else:
            # verificar que exista el usuario
            usuario = auth_server_api.get_usuario(usuario_id)
            if usuario.status_code == 404:
                return {}, 404

        try:
            offset = int(request.args.get('offset', OFFSET_POR_DEFECTO))
            cantidad = int(request.args.get('cantidad', CANTIDAD_POR_DEFECTO))
        except ValueError:
            abort(400)

        media_response = media_server_api.obtener_videos_usuario(usuario_id, offset, cantidad)
        videos = media_response.json()["videos"]
        videos = list(map(self.armar_video_sin_autor, videos))
        return videos, media_response.status_code
