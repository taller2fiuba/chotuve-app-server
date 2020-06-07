#from flask import request
from app.login_requerido_decorator import login_requerido
from .video_base import VideoBaseResource

class VideoReaccion(VideoBaseResource):
    @login_requerido
    def post(self, video_id):
        # post_data = request.get_json(force=True)
        return {"id": video_id}, 200
