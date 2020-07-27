from flask_restful import Resource
from app.models.reaccion import Reaccion
from app.models.contacto import Contacto

class HistoricoResource(Resource):
    def get(self):
        reacciones = Reaccion.cantidad_reacciones()
        contactos = Contacto.cantidad_contactos()
        return  {"total_reacciones": reacciones,
                 "total_contactos": contactos}, 200
