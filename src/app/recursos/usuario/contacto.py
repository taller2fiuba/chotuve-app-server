from flask_restful import Resource
from flask import g
import auth_server_api
from app.login_requerido_decorator import login_requerido

from app.models.contacto import Contacto

class ContactoResource(Resource):
    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual

        contactos = Contacto.obtener_contactos(usuario_id)
        if len(contactos) == 0:
            return []

        response = auth_server_api.obtener_usuarios({'ids': ','.join(map(str, contactos))})
        if response.status_code != 200:
            return response

        ret = [{'id': u['id'], 'email': u['email']} for u in response.json()]

        return ret
