import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioVideoTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_videos_usuario')
    def test_get_mis_videos_sin_videos_devuelve_vacio(self, mock_media, mock_auth):
        mock_media.return_value = []
        mock_auth.return_value = {
            "id": 2,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
        }

        response = self.app.get('/usuario/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_videos_usuario')
    def test_get_mis_videos_con_videos_devuelve_mis_videos(self, mock_media, mock_auth):
        mock_auth.return_value = {
            "id": 2,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
        }

        mock_media.return_value = [{
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

        response = self.app.get('/usuario/video')
        video_response = {
            'id': "5ef4cb51c69cbf0072a6abdb",
            'url': "https://urltest.com/video/123456",
            'titulo': "video test",
            'duracion': 60,
            'creacion': "2020-06-25T16:05:37.091Z",
            'visibilidad': "publico",
            'descripcion': None,
            'cantidad-comentarios': 0,
            "no-me-gustas": 0,
            "me-gustas":0,
            "mi-reaccion": None
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual([video_response], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_videos_usuario_inexistente_da_error(self, mock_auth):
        mock_auth.return_value = None

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(404, response.status_code)
        self.assertEqual({}, response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    def test_get_videos_con_offset_string_da_400(self, mock_auth):
        mock_auth.return_value = {'id': 1234}

        response = self.app.get('/usuario/1234/video?offset="asd"')

        self.assertEqual(400, response.status_code)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_videos_usuario')
    def test_get_videos_de_usuario_sin_videos_devuelve_vacio(self, mock_media, mock_auth):
        autor = {
            "id": 1234,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
        }

        mock_auth.return_value = autor
        mock_media.return_value = []

        response = self.app.get('/usuario/1234/video')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.servicios.media_server.obtener_videos_usuario')
    def test_get_videos_de_usuario_con_videos_devuelve_sus_videos(self, mock_media, mock_auth):
        mock_auth.return_value = {
            "id": 1234,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
        }

        mock_media.return_value = [{
            "descripcion": None,
            "ubicacion": None,
            "visibilidad": "publico",
            "habilitado": True,
            "_id": "5ef4cb51c69cbf0072a6abdb",
            "url": "https://urltest.com/video/123456",
            "titulo": "video test",
            "usuario_id": 1,
            "duracion": 60,
            "time_stamp": "2020-06-25T16:05:37.091Z",
            "__v": 0
        }]

        video_response = {
            'id': "5ef4cb51c69cbf0072a6abdb",
            'url': "https://urltest.com/video/123456",
            'titulo': "video test",
            'duracion': 60,
            'creacion': "2020-06-25T16:05:37.091Z",
            'visibilidad': "publico",
            'descripcion': None,
            'cantidad-comentarios': 0,
            "no-me-gustas": 0,
            "me-gustas":0,
            "mi-reaccion": None
        }

        response = self.app.get('/usuario/1234/video')
        self.assertEqual(200, response.status_code)
        self.assertEqual([video_response], response.json)

if __name__ == '__main__':
    unittest.main()
