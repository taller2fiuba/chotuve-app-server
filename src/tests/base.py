import unittest
from unittest.mock import MagicMock
from flask import g

from app import app, db, login_requerido_decorator
from config import Config

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_object(Config)
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class MockResponse:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json_data = json

    def json(self):
        return self.json_data

class LoginMockTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        g.usuario_actual = 1
        login_requerido_decorator.auth_server_api.autentificar = MagicMock(return_value=MockResponse(200, {'usuario_id': 1}))
