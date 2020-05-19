import unittest
import mock

from tests.base import BaseTestCase

class BaseDeDatosTestCase(BaseTestCase):
    @mock.patch('auth_server_api.requests.delete')
    def test_delete_base_de_datos_exitoso(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 200)
        # TODO cuando haya alguna tabla verificar que esta vacia

    @mock.patch('auth_server_api.requests.delete')
    def test_delete_base_de_datos_de_auth_server_fallido(self, mock_post):
        mock_post.return_value.status_code = 500
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
