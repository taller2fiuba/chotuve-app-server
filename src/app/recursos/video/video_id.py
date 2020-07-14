from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server
import media_server_api
from .video_base import VideoBaseResource

class VideoIdResource(VideoBaseResource):
    @login_requerido
    def get(self, video_id):
        response = media_server_api.obtener_video(video_id)
        if response.status_code != 200:
            return response.json(), response.status_code
        video = response.json()

        autor = auth_server.obtener_usuario(video['usuario_id'])
        if not autor:
            return {}, 404

        return self.armar_video(video, autor), 200
