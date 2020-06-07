from flask import request, abort, g
from app import db
from app.login_requerido_decorator import login_requerido
from app.models.reaccion import Reaccion, TipoReaccion
from .video_base import VideoBaseResource

REACCIONES = {'me-gusta': TipoReaccion.ME_GUSTA,
              'no-me-gusta': TipoReaccion.NO_ME_GUSTA}

class VideoReaccion(VideoBaseResource):
    @login_requerido
    def post(self, video_id):
        if not request.content_type == 'application/json':
            abort(400)

        reaccion = request.get_json().get('reaccion')
        if not reaccion or reaccion not in REACCIONES:
            return {"error": f'La reaccion {reaccion} es inválida'}, 400

        # Buscar la reacción en la base
        # Si no hay una reacción para mi usuario y el video indicado
        #  201 -> reacción creada
        # Si ya hay una reacción
        #  200 -> reacción modificada / eliminada
        query = Reaccion.query
        query = query.filter_by(video=video_id, usuario=g.usuario_actual)
        reaccion_guardada = query.one_or_none()

        if reaccion_guardada:
            reaccion_guardada.tipo = REACCIONES[reaccion]
        else:
            db.session.add(Reaccion(
                video=video_id,
                usuario=g.usuario_actual,
                tipo=REACCIONES[reaccion]))

        db.session.commit()
        return {}, 200 if reaccion_guardada else 201
