import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioVideoTestCase(LoginMockTestCase):
    @mock.patch('media_server_api.requests.get')
    def test_get_mis_videos_sin_videos_devuelve_vacio(self, mock_media):
        mock_media.return_value.json = lambda: []
        mock_media.return_value.status_code = 200
        response = self.app.get('/usuario/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('media_server_api.requests.get')
    def test_get_mis_videos_con_videos_devulve_mis_videos(self, mock_media):
        mock_media.return_value.json = lambda: [{
            "descripcion": None,
            "ubicacion": None,
            "visibilidad": "publico",
            "habilitado": False,
            "_id": "5ef4cb51c69cbf0072a6abdb",
            "url": "https://urltest.com/video/123456",
            "titulo": "video test",
            "usuario_id": 1,
            "duracion": 60,
            "time_stamp": "2020-06-25T16:05:37.091Z",
            "__v": 0
            }]
        mock_media.return_value.status_code = 200
        response = self.app.get('/usuario/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))

    @mock.patch('media_server_api.requests.get')
    def test_get_videos_usuario_inexistente_da_error(self, mock_media):
        mock_media.return_value.json = lambda: {}
        mock_media.return_value.status_code = 404
        response = self.app.get('/usuario/1234/video')

        self.assertEqual(404, response.status_code)
        self.assertEqual({}, response.json)

    @mock.patch('media_server_api.requests.get')
    def test_get_videos_de_usuario_sin_videos_devuelve_vacio(self, mock_media):
        mock_media.return_value.json = lambda: []
        mock_media.return_value.status_code = 200
        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('media_server_api.requests.get')
    def test_get_videos_de_usuario_con_videos_devulve_sus_videos(self, mock_media):
        mock_media.return_value.json = lambda: [{
            "descripcion": None,
            "ubicacion": None,
            "visibilidad": "publico",
            "habilitado": False,
            "_id": "5ef4cb51c69cbf0072a6abdb",
            "url": "https://urltest.com/video/123456",
            "titulo": "video test",
            "usuario_id": 1,
            "duracion": 60,
            "time_stamp": "2020-06-25T16:05:37.091Z",
            "__v": 0
            }]
        mock_media.return_value.status_code = 200
        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))

if __name__ == '__main__':
    unittest.main()
