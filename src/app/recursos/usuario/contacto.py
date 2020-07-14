from flask_restful import Resource
from flask import g

from app.login_requerido_decorator import login_requerido

from app.models.contacto import Contacto
from app.servicios import auth_server

class ContactoResource(Resource):
    @login_requerido
    def get(self, usuario_id=None):
        if not usuario_id:
            usuario_id = g.usuario_actual

        contactos = Contacto.obtener_contactos(usuario_id)
        if len(contactos) == 0:
            return []

        usuarios = auth_server.obtener_usuarios(contactos)
        return [{'id': u['id'], 'email': u['email'], 'foto': u['foto']} for u in usuarios.values()]
