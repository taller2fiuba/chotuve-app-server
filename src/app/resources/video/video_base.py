from flask_restful import Resource

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
                }
        }
