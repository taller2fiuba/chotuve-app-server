from unittest import TestCase
from mock import patch

from app.servicios.servicio_auth_server import AuthServer, AuthServerError

class AuthServerTestCase(TestCase):
    def setUp(self):
        self.patcher_get = patch('requests.get')
        self.mock_get = self.patcher_get.start()
        self.addCleanup(self.patcher_get.stop)

    def test_obtener_usuarios_devuelve_datos_recibidos(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 123}

        auth = AuthServer('http://localhost')

        self.assertEqual({'id': 123}, auth.obtener_usuario(1))
        self.mock_get.assert_called_with('http://localhost/usuario/1')

    def test_obtener_usuarios_ignora_barra_final_url(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json = lambda: {'id': 123}

        auth = AuthServer('http://localhost/')

        self.assertEqual({'id': 123}, auth.obtener_usuario(1))
        self.mock_get.assert_called_with('http://localhost/usuario/1')

    def test_obtener_usuarios_devuelve_none_en_404(self):
        self.mock_get.return_value.status_code = 404
        self.mock_get.return_value.json = lambda: {}

        auth = AuthServer('http://localhost/')

        self.assertIsNone(auth.obtener_usuario(1))
        self.mock_get.assert_called_with('http://localhost/usuario/1')

    def test_obtener_usuarios_lanza_excepcion_en_400(self):
        self.mock_get.return_value.status_code = 400
        self.mock_get.return_value.json = lambda: None

        auth = AuthServer('http://localhost')

        self.assertRaises(AuthServerError, auth.obtener_usuario, 1)
        self.mock_get.assert_called_with('http://localhost/usuario/1')
