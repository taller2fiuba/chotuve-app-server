from datetime import datetime
from flask import request, abort

from flask_restful import Resource
from app.models.reaccion import Reaccion
from app.models.comentario import Comentario

class StatsResource(Resource):
    def get(self):
        f_inicio = request.args.get('inicio', None)
        f_final = request.args.get('fin', None)

        if not f_inicio or not f_final:
            abort(400)

        try:
            f_inicio = datetime.strptime(f_inicio, "%Y-%m-%d")
            f_final = datetime.strptime(f_final, "%Y-%m-%d")
        except ValueError:
            return {}, 400

        reacciones = Reaccion.reacciones_por_fecha(f_inicio, f_final)
        comentarios = Comentario.comentarios_por_fecha(f_inicio, f_final)

        return  {"reacciones":reacciones, "comentarios": comentarios}, 200
