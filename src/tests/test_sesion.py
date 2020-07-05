import unittest
import mock

from tests.base import BaseTestCase

class SesionTestCase(BaseTestCase):
    @mock.patch('auth_server_api.requests.post')
    def test_post_login_exitoso(self, mock_post):
        mock_post.return_value.json = lambda: {'auth_token': '11111', 'id': 1}
        mock_post.return_value.status_code = 200
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'auth_token': '11111', 'id': 1}, response.json)

    @mock.patch('auth_server_api.requests.post')
    def test_post_login_fallido(self, mock_post):
        mock_post.return_value.json = lambda: {'mensaje': 'Email o constraseña invalidos'}
        mock_post.return_value.status_code = 400
        response = self.app.post('/usuario', json={
            'email': 'value', 'password': 'data'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual({'mensaje': 'Email o constraseña invalidos'}, response.json)

if __name__ == '__main__':
    unittest.main()
