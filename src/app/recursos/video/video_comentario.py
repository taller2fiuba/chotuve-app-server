from flask import request, abort, g

from app import db
from app.login_requerido_decorator import login_requerido
from app.models.comentario import Comentario, MAX_LEN_COMENTARIO
from app.servicios import auth_server, media_server

from .video_base import VideoBaseResource

CANTIDAD_POR_DEFECTO = 10
USUARIO_ELIMINADO = '<eliminado>'

class VideoComentario(VideoBaseResource):
    @login_requerido
    def post(self, video_id):
        if not 'application/json' in request.content_type:
            abort(400)

        comentario = request.get_json().get('comentario')
        if not isinstance(comentario, str) or not 0 < len(comentario) <= MAX_LEN_COMENTARIO:
            return {"error": f'El comentario {comentario} es inválido'}, 400

        if not media_server.obtener_video(video_id):
            return {"error": "El video no existe."}, 404

        db.session.add(Comentario(
            video=video_id,
            usuario=g.usuario_actual,
            comentario=comentario
        ))

        db.session.commit()
        return {}, 201

    @login_requerido
    def get(self, video_id):
        cantidad = request.args.get('cantidad', CANTIDAD_POR_DEFECTO)
        offset = request.args.get('offset', 0)
        query = Comentario.query.filter_by(video=video_id)
        query = query.offset(offset).limit(cantidad)
        comentarios = query.all()
        autores = auth_server.obtener_usuarios({c.usuario for c in comentarios})

        return [{
            'autor': autores.get(comentario.usuario, USUARIO_ELIMINADO),
            'fecha': comentario.fecha.isoformat(),
            'comentario': comentario.comentario
        } for comentario in comentarios], 200
