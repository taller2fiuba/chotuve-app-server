import unittest
import mock

from tests.base import BaseTestCase

class BaseDeDatosTestCase(BaseTestCase):
    @mock.patch('media_server_api.limpiar_base_de_datos')
    @mock.patch('app.servicios.auth_server.limpiar_base_de_datos')
    def test_delete_base_de_datos_exitoso(self, mock_auth, mock_media):
        mock_auth.return_value = True
        mock_media.return_value.status_code = 200
        mock_media.return_value.json = lambda: {}
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 200)

    @mock.patch('media_server_api.limpiar_base_de_datos')
    @mock.patch('app.servicios.auth_server.limpiar_base_de_datos')
    def test_delete_base_de_datos_de_auth_server_fallido(self, mock_auth, mock_media):
        mock_auth.return_value = False
        mock_media.return_value.status_code = 200
        mock_media.return_value.json = lambda: {}
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
