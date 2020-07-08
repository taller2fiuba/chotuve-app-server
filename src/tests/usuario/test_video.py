import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioVideoTestCase(LoginMockTestCase):
    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_mis_videos_sin_videos_devuelve_vacio(self, mock_media, mock_auth):

        mock_media.return_value.json = lambda: []
        mock_media.return_value.status_code = 200

        perfil = {
            "id": 2,
            "email": "test@test.com",
            "password": "pswd",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None
            }

        mock_auth.return_value.json = lambda: perfil
        mock_auth.return_value.status_code = 200

        response = self.app.get('/usuario/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_mis_videos_con_videos_devulve_mis_videos(self, mock_media, mock_auth):

        perfil = {
            "id": 2,
            "email": "test@test.com",
            "password": "pswd",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None
            }

        mock_auth.return_value.json = lambda: perfil
        mock_auth.return_value.status_code = 200

        video = {
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
            }

        mock_media.return_value.json = lambda: [video]
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/video')

        respuesta = [{
            'id': "5ef4cb51c69cbf0072a6abdb",
            'url': "https://urltest.com/video/123456",
            'titulo': "video test",
            'duracion': 60,
            'creacion': "2020-06-25T16:05:37.091Z",
            'visibilidad': "publico",
            'descripcion': None,
            'autor': {
                'usuario_id': 2,
                'nombre': None,
                'apellido': None,
                'email': "test@test.com"
            },
            "no-me-gustas": 0,
            "me-gustas": 0,
            "mi-reaccion": None
        }]

        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_videos_usuario_inexistente_da_error(self, mock_media, mock_auth):
        mock_auth.return_value.json = lambda: {}
        mock_auth.return_value.status_code = 404

        mock_media.return_value.json = lambda: []
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(404, response.status_code)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_videos_de_usuario_sin_videos_devuelve_vacio(self, mock_media, mock_auth):
        perfil = {
            "id": 1234,
            "email": "test@test.com",
            "password": "pswd",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None
            }

        mock_auth.return_value.json = lambda: perfil
        mock_media.return_value.status_code = 200

        mock_media.return_value.json = lambda: []
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_videos_de_usuario_con_videos_devulve_sus_videos(self, mock_media, mock_auth):
        perfil = {
            "id": 1234,
            "email": "test@test.com",
            "password": "pswd",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None
            }

        mock_auth.return_value.json = lambda: perfil
        mock_media.return_value.status_code = 200

        video = {
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
            }

        mock_media.return_value.json = lambda: [video]
        mock_media.return_value.status_code = 200

        respuesta = [{
            'id': "5ef4cb51c69cbf0072a6abdb",
            'url': "https://urltest.com/video/123456",
            'titulo': "video test",
            'duracion': 60,
            'creacion': "2020-06-25T16:05:37.091Z",
            'visibilidad': "publico",
            'descripcion': None,
            'autor': {
                'usuario_id': 1234,
                'nombre': None,
                'apellido': None,
                'email': "test@test.com"
            },
            "no-me-gustas": 0,
            "me-gustas": 0,
            "mi-reaccion": None
        }]
        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

if __name__ == '__main__':
    unittest.main()
