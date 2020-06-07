from flask import g
from flask_restful import Resource
from app.models.reaccion import Reaccion, TipoReaccion

REACCIONES = {TipoReaccion.ME_GUSTA: 'me-gusta', 
              TipoReaccion.NO_ME_GUSTA: 'no-me-gusta'}

class VideoBaseResource(Resource):
    def armar_video(self, video, autor):
        return {
            'id': video['_id'],
            'url': video['url'],
            'titulo': video['titulo'],
            'duracion': video['duracion'],
            'creacion': video['time_stamp'],
            'visibilidad': video['visibilidad'],
            'descripcion': video['descripcion'],
            'autor': {
                'usuario_id': autor['id'],
                'nombre': autor['nombre'],
                'apellido': autor['apellido'],
                'email': autor['email']
            },
            "no-me-gustas": Reaccion.contar_reacciones(video['_id'],
                                                       TipoReaccion.NO_ME_GUSTA),
            "me-gustas": Reaccion.contar_reacciones(video['_id'],
                                                    TipoReaccion.ME_GUSTA),
            "mi-reaccion": REACCIONES[Reaccion.obtener_reaccion(video['_id'],
                                                     g.usuario_actual)]
        }
