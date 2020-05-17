import unittest
import mock

from tests.base import BaseTestCase

class LoginRequeridoDecoratorTestCase(BaseTestCase):
    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('auth_server_api.autentificar')
    def test_middleware_autenticacion_exitosa(self, mock_autenticacion, mock_get_usuario):
        mock_autenticacion.return_value.status_code = 200
        mock_autenticacion.return_value.json = lambda: {'usuario_id': '3'}
        mock_get_usuario.return_value.status_code = 200
        mock_get_usuario.return_value.json = lambda: {'email': 'test@test.com'}
        token_valido = 'token_valido'
        response = self.app.get('/usuario/1', headers={
            'Authorization': f'Bearer {token_valido}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@test.com')

    @mock.patch('auth_server_api.autentificar')
    def test_middleware_autenticacion_fallida(self, mock_autenticacion):
        mock_autenticacion.return_value.status_code = 403
        mock_autenticacion.return_value.json = lambda: {}
        token_invalido = 'token_invalido'
        response = self.app.get('/usuario/1', headers={
            'Authorization': f'Bearer {token_invalido}'})
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
