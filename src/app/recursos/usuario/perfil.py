from flask_restful import Resource
from flask import request, g
import auth_server_api
import media_server_api
from app.login_requerido_decorator import login_requerido
from app.models.contacto import Contacto
from app.models.solicitud_contacto import SolicitudContacto

class PerfilUsuarioResource(Resource):
    @login_requerido
    def get(self, usuario_id=None):
        if usuario_id is None:
            usuario_id = g.usuario_actual

        response = auth_server_api.get_perfil(usuario_id)
        if response.status_code != 200:
            return response.json(), response.status_code

        perfil = response.json()
        perfil['cantidad-contactos'] = Contacto.obtener_cantidad_contactos(usuario_id)
        videos = media_server_api.obtener_videos_usuario(usuario_id, 0, 0).json()
        perfil["cantidad-videos"] = videos["cantidad_de_videos"]

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
        if not post_data: #no hay body
            return {}, 400
        if not all(parametros in post_data for parametros in campos_requeridos):
            return {}, 400

        nombre = post_data['nombre']
        apellido = post_data['apellido']
        telefono = post_data['telefono']
        direccion = post_data['direccion']
        foto = post_data['foto']

        response = auth_server_api.actualizar_perfil_usuario(nombre, apellido, telefono, direccion,
                                                             foto)

        return response.json(), response.status_code
