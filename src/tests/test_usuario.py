import unittest
import mock

from app import app


class UsuarioTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_exitoso(self, mock_post):
        mock_post.return_value.json = lambda: {'Token': '11111'}
        mock_post.return_value.status_code = 201
        response = self.app.post('/usuario', json={
            'mail': 'value', 'contraseña': 'data'})
        self.assertEqual({'Token': '11111'}, response.json)
        self.assertEqual(response.status_code, 201)

    @mock.patch('auth_server_api.requests.post')
    def test_post_signup_fallido(self, mock_post):
        mock_post.return_value.json = lambda: {'Mensaje de error': 'Mail en uso'}
        mock_post.return_value.status_code = 400
        response = self.app.post('/usuario', json={
            'mail': 'value', 'contraseña': 'data'})
        self.assertEqual({'Mensaje de error': 'Mail en uso'}, response.json)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
