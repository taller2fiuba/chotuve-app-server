#pylint: skip-file
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from .resources import Ping
from .resources import Video
from .resources import Usuario
from .resources import Sesion

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
API = Api(app)

API.add_resource(Ping, '/ping')

API.add_resource(Video, '/video')

API.add_resource(Usuario, '/usuario')

API.add_resource(Sesion, '/usuario/sesion')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from app import models
