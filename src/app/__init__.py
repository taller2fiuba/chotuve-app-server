#pylint: skip-file
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, configurar_logger
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
configurar_logger()
log = logging.getLogger(__name__)

from .resources import Ping, Sesion, UsuarioResource, BaseDeDatosResource, PerfilUsuarioResource, PerfilOtroUsuarioResource, VideoResource, VideoIdResource

api.add_resource(Ping, '/ping')
api.add_resource(VideoResource, '/video')
api.add_resource(VideoIdResource, '/video/<video_id>')
api.add_resource(UsuarioResource, '/usuario', '/usuario/')
api.add_resource(UsuarioResource, '/usuario/<int:usuario_id>', methods=["GET"], endpoint='UsuarioConIdResource')
api.add_resource(PerfilUsuarioResource, '/usuario/perfil', methods=["PUT", "GET"], endpoint='PerfilUsuario')
api.add_resource(PerfilOtroUsuarioResource, '/usuario/perfil/<int:usuario_id>', methods=["GET"], endpoint='PerfilOtroUsuario')
api.add_resource(Sesion, '/usuario/sesion')
api.add_resource(BaseDeDatosResource, '/base_de_datos')
@app.errorhandler(Exception)
def unhandled_exception(e):
    tb = traceback.format_exc()
    log.warn(f'Excepcion no manejada: {tb}')
    return {'mensaje': str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

log.info(f'Iniciando version de la app: {Config.APP_VERSION}')
