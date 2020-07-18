import unittest
import mock

from tests.base import BaseTestCase

class SesionTestCase(BaseTestCase):
    @mock.patch('app.servicios.auth_server.iniciar_sesion')
    def test_post_login_exitoso(self, mock_auth):
        mock_auth.return_value = 'auth_token', 1
        response = self.app.post('/usuario/sesion', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'auth_token': 'auth_token', 'id': 1}, response.json)
        mock_auth.assert_called_with('value', 'data')

    @mock.patch('app.servicios.auth_server.iniciar_sesion')
    def test_post_login_fallido(self, mock_auth):
        mock_auth.return_value = None
        response = self.app.post('/usuario/sesion', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual({'mensaje': 'Email o constraseña invalidos'}, response.json)
        mock_auth.assert_called_with('value', 'data')

if __name__ == '__main__':
    unittest.main()
