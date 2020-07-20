from flask_restful import Resource
from flask import request, g
from app.login_requerido_decorator import login_requerido
from app.models.contacto import Contacto
from app.models.solicitud_contacto import SolicitudContacto
from app.servicios import auth_server, media_server

class PerfilUsuarioResource(Resource):
    @login_requerido
    def get(self, usuario_id=None):
        if usuario_id is None:
            usuario_id = g.usuario_actual

        perfil = auth_server.obtener_usuario(usuario_id)
        if not perfil:
            return {}, 404

        perfil['cantidad-contactos'] = Contacto.obtener_cantidad_contactos(usuario_id)

        con_privados = usuario_id == g.usuario_actual or \
                       Contacto.es_contacto(usuario_id, g.usuario_actual)

        perfil["cantidad-videos"] = media_server.obtener_cantidad_videos(usuario_id, con_privados)

        if usuario_id != g.usuario_actual:
            if Contacto.es_contacto(g.usuario_actual, usuario_id):
                perfil['estado-contacto'] = 'contacto'
            elif SolicitudContacto.hay_solicitud(g.usuario_actual, usuario_id):
                perfil['estado-contacto'] = 'solicitud-enviada'
            elif SolicitudContacto.hay_solicitud(usuario_id, g.usuario_actual):
                perfil['estado-contacto'] = 'solicitud-pendiente'
            else:
                perfil['estado-contacto'] = None
        return perfil, 200

    @login_requerido
    def put(self):
        campos_requeridos = ('nombre', 'apellido')
        post_data = request.get_json()
        if not post_data or not all(parametros in post_data for parametros in campos_requeridos):
            return {}, 400

        if not auth_server.actualizar_usuario(g.usuario_actual, post_data):
            return {}, 404
        return {}, 200
