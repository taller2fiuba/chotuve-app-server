from flask_restful import Resource
from flask import request, g
import media_server_api
import auth_server_api
from app.login_requerido_decorator import login_requerido
from app.recursos.video.video_base import VideoBaseResource

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

        offset = request.args.get('offset', OFFSET_POR_DEFECTO)
        cantidad = request.args.get('cantidad', CANTIDAD_POR_DEFECTO)
        if not isdigit(offset) or not isdigit(cantidad):
            return {}, 500
        media_response = media_server_api.obtener_videos_usuario(usuario_id, offset, cantidad)
        videos = media_response.json()
        for video in range(len(videos)):
            videos[video] = VideoBaseResource.armar_video(videos[video], usuario)

        return response, media_response.status_code
