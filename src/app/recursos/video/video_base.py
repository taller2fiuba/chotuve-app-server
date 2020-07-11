from flask import g
from flask_restful import Resource
from app.models.reaccion import Reaccion, TipoReaccion
from app.models.comentario import Comentario

REACCIONES = {TipoReaccion.ME_GUSTA: 'me-gusta',
              TipoReaccion.NO_ME_GUSTA: 'no-me-gusta'}

class VideoBaseResource(Resource):
    def armar_video(self, video, autor):
        video = self.armar_video_sin_autor(video)
        video.update(self.armar_autor(autor))
        return video

    def armar_video_sin_autor(self, video):
        return {
            'id': video['_id'],
            'url': video['url'],
            'titulo': video['titulo'],
            'duracion': video['duracion'],
            'creacion': video['time_stamp'],
            'visibilidad': video['visibilidad'],
            'descripcion': video['descripcion'],
            'cantidad-comentarios': Comentario.contar_comentarios(video['_id']),
            "no-me-gustas": Reaccion.contar_reacciones(video['_id'],
                                                       TipoReaccion.NO_ME_GUSTA),
            "me-gustas": Reaccion.contar_reacciones(video['_id'],
                                                    TipoReaccion.ME_GUSTA),
            "mi-reaccion": REACCIONES.get(Reaccion.obtener_reaccion(video['_id'],
                                                                    g.usuario_actual))
        }

    def armar_autor(self, autor):
        return {
            'autor': {
                'usuario_id': autor['id'],
                'email': autor['email'],
                'nombre': autor['nombre'],
                'apellido': autor['apellido'],
                'foto': autor['foto']
            },
        }