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
api = Api(app)

from .resources import Ping, Sesion, UsuarioResource, BaseDeDatosResource, VideoResource, VideoIdResource
api.add_resource(Ping, '/ping')
api.add_resource(VideoResource, '/video')
api.add_resource(VideoIdResource, '/video/<video_id>')
api.add_resource(UsuarioResource, '/usuario', '/usuario/')
api.add_resource(UsuarioResource, '/usuario/<int:usuario_id>', methods=["GET"], endpoint='UsuarioConIdResource')
api.add_resource(Sesion, '/usuario/sesion')
api.add_resource(BaseDeDatosResource, '/base_de_datos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
