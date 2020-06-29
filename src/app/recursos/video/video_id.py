from app.login_requerido_decorator import login_requerido
import auth_server_api
import media_server_api
from .video_base import VideoBaseResource

class VideoIdResource(VideoBaseResource):
    @login_requerido
    def get(self, video_id):
        response = media_server_api.obtener_video(video_id)
        if response.status_code != 200:
            return response.json(), response.status_code
        video = response.json()

        response = auth_server_api.get_usuario(video['usuario_id'])
        if response.status_code != 200:
            return response.json(), response.status_code
        autor = response.json()

        return self.armar_video(video, autor), response.status_code
