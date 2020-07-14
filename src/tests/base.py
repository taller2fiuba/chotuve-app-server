import unittest
from unittest.mock import MagicMock

from app import app, db, login_requerido_decorator
from app.repositorios import usuario_actual_repositorio
from config import Config

from app.servicios.servicio_auth_server import AuthServerError
from app.servicios.servicio_media_server import MediaServerError

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_object(Config)
        db.create_all()
        db.session.commit()

    def auth_server_error(self, status_code=500, data=None):
        def auth_error(*_, **__):
            raise AuthServerError(MagicMock(status_code=status_code, json=lambda: data))
        return auth_error
    
    def media_server_error(self, status_code=500, data=None):
        def media_error(*_, **__):
            raise MediaServerError(MagicMock(status_code=status_code, json=lambda: data))
        return media_error

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class LoginMockTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        usuario_actual_repositorio.get_usuario_actual = MagicMock(return_value=1)
        login_requerido_decorator.auth_server.autenticar = MagicMock(return_value=1)
