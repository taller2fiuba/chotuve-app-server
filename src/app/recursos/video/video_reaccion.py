from flask import request, abort, g

from app import db
from app.login_requerido_decorator import login_requerido
from app.models.reaccion import Reaccion, TipoReaccion
from app.servicios import auth_server, media_server, notificador

from .video_base import VideoBaseResource


REACCIONES = {'me-gusta': TipoReaccion.ME_GUSTA,
              'no-me-gusta': TipoReaccion.NO_ME_GUSTA}

class VideoReaccion(VideoBaseResource):
    @login_requerido
    def post(self, video_id):
        if not 'application/json' in request.content_type:
            abort(400)

        reaccion = request.get_json().get('reaccion')
        if not reaccion or reaccion not in REACCIONES:
            return {"error": f'La reaccion {reaccion} es inválida'}, 400

        video = media_server.obtener_video(video_id)
        if not video:
            return {"error": "El video no existe."}, 404

        query = Reaccion.query
        query = query.filter_by(video=video_id, usuario=g.usuario_actual)
        reaccion_guardada = query.one_or_none()

        if reaccion_guardada:
            if reaccion_guardada.tipo == REACCIONES[reaccion]:
                db.session.delete(reaccion_guardada)
            else:
                reaccion_guardada.tipo = REACCIONES[reaccion]
        else:
            db.session.add(Reaccion(
                video=video_id,
                usuario=g.usuario_actual,
                tipo=REACCIONES[reaccion]))

        db.session.commit()
        if not reaccion_guardada and reaccion == 'me-gusta':
            notificador.reaccionar_me_gusta_video(video,
                                                  auth_server.obtener_usuario(g.usuario_actual))
        return {}, 200 if reaccion_guardada else 201
