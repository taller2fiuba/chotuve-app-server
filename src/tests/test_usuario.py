import unittest
import mock

from tests.base import BaseTestCase, LoginMockTestCase

class UsuarioTestCase(BaseTestCase):
    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_exitoso(self, mock_post):
        mock_post.return_value.json = lambda: {'Token': '11111'}
        mock_post.return_value.status_code = 201
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual({'Token': '11111'}, response.json)

    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_fallido(self, mock_post):
        mock_post.return_value.json = lambda: {'Mensaje de error': 'Mail en uso'}
        mock_post.return_value.status_code = 400
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual({'Mensaje de error': 'Mail en uso'}, response.json)

class UsuarioLoginMockTestCase(LoginMockTestCase):

    @mock.patch('auth_server_api.requests.get')
    def test_get_usuario_por_id(self, mock_get):
        mock_get.return_value.json = lambda: {'email': 'test@test'}
        mock_get.return_value.status_code = 200
        response = self.app.get('/usuario/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    def test_get_usuario_sin_id_es_el_actual(self, mock_get_usuario):
        mock_get_usuario.return_value.json = lambda: {'email': 'test@test'}
        mock_get_usuario.return_value.status_code = 200
        response = self.app.get('/usuario')
        mock_get_usuario.assert_called_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'email': 'test@test'}, response.json)

if __name__ == '__main__':
    unittest.main()
