from flask_restful import Resource
from flask import request, g
import media_server_api
import auth_server_api
from app.login_requerido_decorator import login_requerido
from app.recursos.video.video_base import formatear_video

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10

class VideoUsuarioResource(Resource):
    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual
        usuario = auth_server_api.get_usuario(usuario_id)
        if usuario.status_code == 404: #no existe el usuario
            return {}, 404

        try:
            offset = int(request.args.get('offset', OFFSET_POR_DEFECTO))
            cantidad = int(request.args.get('cantidad', CANTIDAD_POR_DEFECTO))
        except ValueError:
            return {}, 500

        media_response = media_server_api.obtener_videos_usuario(usuario_id, offset, cantidad)
        videos = media_response.json()
        datos_usuario = usuario.json()
        #datos_usuario["cantidad_de_videos"] = len(videos)
        videos = [formatear_video(video, ) for video in videos]

        return videos, media_response.status_code
