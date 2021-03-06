from flask_restful import Resource
from flask import request, g, abort

from app.login_requerido_decorator import login_requerido

from app import db
from app.models.solicitud_contacto import SolicitudContacto
from app.models.contacto import Contacto
from app.servicios import auth_server, notificador

class SolicitudContactoResource(Resource):
    @login_requerido
    def get(self):
        data = SolicitudContacto.obtener_solicitudes_pendientes(g.usuario_actual)
        if len(data) == 0:
            return []

        usuarios = [s.usuario_emisor for s in data]
        data_usuarios = auth_server.obtener_usuarios(usuarios)

        ret = []
        for solicitud in data:
            data_usuario = data_usuarios.get(
                solicitud.usuario_emisor,
                {'email': '<eliminado>', 'foto': None}
            )
            ret.append({
                'id': solicitud.id,
                'usuario_id': solicitud.usuario_emisor,
                'email': data_usuario['email'],
                'foto': data_usuario['foto']
            })

        return ret

    @login_requerido
    def post(self): # pylint: disable=too-many-return-statements
        post_data = request.get_json()
        if not 'usuario_id' in post_data:
            return {'mensaje': 'Falta usuario_id.'}, 400

        usuario_receptor = post_data['usuario_id']

        if usuario_receptor == g.usuario_actual:
            return {'mensaje': 'No podés enviarte una solicitud a vos mismo'}, 400

        if SolicitudContacto.hay_solicitud(g.usuario_actual, usuario_receptor):
            return {'mensaje': 'Ya hay una solicitud pendiente.'}, 400

        if SolicitudContacto.hay_solicitud(usuario_receptor, g.usuario_actual):
            return {'mensaje': 'Debe aceptar la solicitud'}, 400

        if Contacto.es_contacto(g.usuario_actual, usuario_receptor):
            return {'mensaje': 'El usuario ya es un contacto'}, 400

        receptor = auth_server.obtener_usuario(usuario_receptor)

        if not receptor:
            return {}, 404

        solicitud = SolicitudContacto(usuario_emisor=g.usuario_actual,
                                      usuario_receptor=usuario_receptor)
        db.session.add(solicitud)
        db.session.commit()
        notificador.enviar_solicitud_contacto(auth_server.obtener_usuario(g.usuario_actual),
                                              receptor)
        return {}, 201

    @login_requerido
    def put(self, solicitud_id):
        post_data = request.get_json()
        accion = post_data.get('accion')
        if accion not in ('aceptar', 'rechazar'):
            return {'mensaje': 'Acción inválida'}, 400

        solicitud = SolicitudContacto.obtener_por_id(solicitud_id)
        if not solicitud or solicitud.usuario_receptor != g.usuario_actual:
            abort(404)

        if accion == 'aceptar':
            contacto = Contacto(usuario_1=solicitud.usuario_emisor,
                                usuario_2=solicitud.usuario_receptor)
            db.session.add(contacto)

        db.session.delete(solicitud)
        db.session.commit()
        if accion == 'aceptar':
            usuario_actual = auth_server.obtener_usuario(g.usuario_actual)
            usuario_emisor = auth_server.obtener_usuario(solicitud.usuario_emisor)
            notificador.aceptar_solicitud_contacto(usuario_actual, usuario_emisor)
        return {}

    @login_requerido
    def delete(self, solicitud_id):
        solicitud = SolicitudContacto.obtener_por_id(solicitud_id)
        if not solicitud or solicitud.usuario_emisor != g.usuario_actual:
            abort(404)

        db.session.delete(solicitud)
        db.session.commit()
        return {}
