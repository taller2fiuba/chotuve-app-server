from flask_restful import Resource
from flask import request, g
import media_server_api
import auth_server_api
from app.login_requerido_decorator import login_requerido

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
        offset = int(request.args.get('offset', OFFSET_POR_DEFECTO))
        cantidad = int(request.args.get('cantidad', CANTIDAD_POR_DEFECTO))
        media_response = media_server_api.obtener_videos_usuario(usuario_id, offset, cantidad)
        response = {
            "perfil": usuario.json(),
            "videos": media_response.json(),
            "cantidad_de_videos": len(media_response.json())
            }
        return response, media_response.status_code
