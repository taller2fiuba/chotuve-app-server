from app.login_requerido_decorator import login_requerido
from app.servicios import auth_server, media_server
from .video_base import VideoBaseResource

class VideoIdResource(VideoBaseResource):
    @login_requerido
    def get(self, video_id):
        video = media_server.obtener_video(video_id)
        if not video:
            return {}, 404

        autor = auth_server.obtener_usuario(video['usuario_id'])
        if not autor:
            return {}, 404

        return self.armar_video(video, autor), 200
