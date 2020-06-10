from flask import request, abort, g
from app import db
from app.login_requerido_decorator import login_requerido
from app.models.comentario import Comentario, MAX_LEN_COMENTARIO
import media_server_api
import auth_server_api
from .video_base import VideoBaseResource

CANTIDAD_POR_DEFECTO = 10
USUARIO_ELIMINADO = '<eliminado>'

class VideoComentario(VideoBaseResource):
    @login_requerido
    def post(self, video_id):
        if not request.content_type == 'application/json':
            abort(400)

        comentario = request.get_json().get('comentario')
        if not isinstance(comentario, str) or not 0 < len(comentario) <= MAX_LEN_COMENTARIO:
            return {"error": f'El comentario {comentario} es inválido'}, 400

        response = media_server_api.obtener_video(video_id)
        if response.status_code != 200:
            abort(response.status_code)

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
        params = {
            'ids': ','.join({str(comentario.usuario) for comentario in comentarios}),
            'cantidad': cantidad
        }
        autores = {u['id']: u
                   for u in auth_server_api.obtener_usuarios(params).json()}

        return [{
            'autor': autores.get(comentario.usuario, USUARIO_ELIMINADO),
            'fecha': str(comentario.fecha),
            'comentario': comentario.comentario
        } for comentario in comentarios], 200
