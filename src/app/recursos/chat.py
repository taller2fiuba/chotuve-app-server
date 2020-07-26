from flask import g, request
from flask_restful import Resource
from app.login_requerido_decorator import login_requerido

from app.models.contacto import Contacto
from app.servicios import chat, auth_server, notificador

class ChatResource(Resource):
    @login_requerido
    def post(self, destinatario_id):
        data = request.json
        if not data or not 'mensaje' in data:
            return {'mensaje': 'Falta el mensaje'}, 400
        destinatario = auth_server.obtener_usuario(destinatario_id)
        if not destinatario:
            return {'mensaje': 'El destinatario no existe.'}, 404
        if not Contacto.es_contacto(g.usuario_actual, destinatario_id):
            return {'mensaje': 'El destinatario no es contacto.'}, 400

        chat.enviar_mensaje(data['mensaje'], g.usuario_actual, destinatario_id)
        notificador.enviar_mensaje_chat(data['mensaje'],
                                        auth_server.obtener_usuario(g.usuario_actual),
                                        destinatario)
        return {}, 201
