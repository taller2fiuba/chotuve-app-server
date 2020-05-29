#pylint: skip-file
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
API = Api(app)

from .resources import Ping, Video, Sesion, UsuarioResource, BaseDeDatosResource
API.add_resource(Ping, '/ping')
API.add_resource(Video, '/video')
API.add_resource(UsuarioResource, '/usuario', '/usuario/')
API.add_resource(UsuarioResource, '/usuario/<int:usuario_id>', methods=["GET"], endpoint='UsuarioConIdResource')
API.add_resource(UsuarioResource, '/usuario/perfil', methods=["PUT"], endpoint='PerfilUsuario')
API.add_resource(Sesion, '/usuario/sesion')
API.add_resource(BaseDeDatosResource, '/base_de_datos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
