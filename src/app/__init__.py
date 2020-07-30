#pylint: skip-file
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import logging
import traceback

from config import Config, configurar_logger

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
configurar_logger()
log = logging.getLogger(__name__)
CORS(app)

from .servicios import configurar_servicios
configurar_servicios(app, log)

from .recursos import *

api.add_resource(Ping, '/ping')
api.add_resource(VideoResource, '/video')
api.add_resource(VideoIdResource, '/video/<video_id>')
api.add_resource(VideoReaccion, '/video/<video_id>/reaccion')
api.add_resource(VideoComentario, '/video/<video_id>/comentario')
api.add_resource(UsuarioResource, '/usuario', '/usuario/')
api.add_resource(UsuarioResource, '/usuario/<int:usuario_id>', methods=["GET"], endpoint='UsuarioConIdResource')
api.add_resource(PerfilUsuarioResource, '/usuario/perfil')
api.add_resource(PerfilUsuarioResource, '/usuario/<int:usuario_id>/perfil', methods=["GET"], endpoint='PerfilOtroUsuario')
api.add_resource(Sesion, '/usuario/sesion')
api.add_resource(UsuarioClaveResource, '/usuario/clave')
api.add_resource(BaseDeDatosResource, '/base_de_datos')
api.add_resource(SolicitudContactoResource, '/usuario/solicitud-contacto')
api.add_resource(SolicitudContactoResource,
                 '/usuario/solicitud-contacto/<int:solicitud_id>',
                 endpoint='SolicitudContactoIdResource')
api.add_resource(ContactoResource, '/usuario/contacto')
api.add_resource(ContactoResource,
                 '/usuario/<int:usuario_id>/contacto',
                 endpoint='ContactoIdResource')
api.add_resource(VideoUsuarioResource,
                 '/usuario/<int:usuario_id>/video',
                 endpoint='UsuarioVideoIdResource')
api.add_resource(VideoUsuarioResource,
                 '/usuario/video',
                 endpoint='UsuarioVideoResource')
api.add_resource(ChatResource, '/chat/<int:destinatario_id>')
api.add_resource(HistoricoResource, '/stats/historico')
api.add_resource(StatsResource, '/stats')

from app.servicios.servicio_auth_server import AuthServerError
@app.errorhandler(AuthServerError)
def auth_error(e):
    log.error('Error del auth server: (%r) %r', e.status_code, e.payload)
    return e.payload, e.status_code

from app.servicios.servicio_media_server import MediaServerError
@app.errorhandler(MediaServerError)
def media_error(e):
    log.error('Error del media server: (%r) %r', e.status_code, e.payload)
    return e.payload, e.status_code

@app.errorhandler(Exception)
def unhandled_exception(e):
    tb = traceback.format_exc()
    log.error(f'Excepcion no manejada: {tb}')
    return {'mensaje': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

log.info(f'Iniciando version de la app: {Config.APP_VERSION}')
