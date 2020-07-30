from flask_restful import Resource
from app.models.reaccion import Reaccion
from app.models.comentario import Comentario

class HistoricoResource(Resource):
    def get(self):
        reacciones = Reaccion.cantidad_reacciones()
        comentarios = Comentario.cantidad_comentarios()
        return  {"total_reacciones": reacciones,
                 "total_comentarios": comentarios}, 200
