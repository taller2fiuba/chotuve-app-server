import unittest
import mock

from tests.base import LoginMockTestCase

class UsuarioVideoTestCase(LoginMockTestCase):
    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_mis_videos_sin_videos_devuelve_vacio(self, mock_media, mock_auth):

        mock_media.return_value.json = lambda: {
            "videos": [],
            "total": 0
        }
        mock_media.return_value.status_code = 200

        perfil = {
            "id": 2,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
        }

        mock_auth.return_value.json = lambda: perfil
        mock_auth.return_value.status_code = 200

        response = self.app.get('/usuario/video')

        respuesta = {
            "autor": {
                "usuario_id": 2,
                "email": "test@test.com",
                "nombre": None,
                "apellido": None,
                "foto": "url/foto"
            },
            "videos":[],
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

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
            "telefono": None,
            "foto": "url/foto"
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

        mock_media.return_value.json = lambda: {
            "videos": [video],
            "total": 1
        }
        mock_media.return_value.status_code = 200

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

        respuesta = {
            "autor": {
                "usuario_id": 2,
                "email": "test@test.com",
                "nombre": None,
                "apellido": None,
                "foto": "url/foto"
            },
            "videos": [video_response]
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_videos_usuario_inexistente_da_error(self, mock_media, mock_auth):
        mock_auth.return_value.json = lambda: {}
        mock_auth.return_value.status_code = 404

        mock_media.return_value.json = lambda: {
            "videos": [0],
            "total": 0
        }
        mock_media.return_value.status_code = 200

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(404, response.status_code)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    def test_get_videos_con_offset_string_da_400(self, mock_auth):
        mock_auth.return_value.json = lambda: {}
        mock_auth.return_value.status_code = 200

        response = self.app.get('/usuario/1234/video?offset="asd"')

        self.assertEqual(400, response.status_code)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
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

        mock_auth.return_value.json = lambda: autor
        mock_media.return_value.status_code = 200

        mock_media.return_value.json = lambda: {
            "videos": [],
            "total": 0
        }
        mock_media.return_value.status_code = 200

        respuesta = {
            "autor": {
                "usuario_id": 1234,
                "email": "test@test.com",
                "nombre": None,
                "apellido": None,
                "foto": "url/foto"
            },
            "videos":[]
        }

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_videos_usuario')
    def test_get_videos_de_usuario_con_videos_devulve_sus_videos(self, mock_media, mock_auth):
        perfil = {
            "id": 1234,
            "email": "test@test.com",
            "nombre": None,
            "apellido": None,
            "direccion": None,
            "telefono": None,
            "foto": "url/foto"
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

        mock_media.return_value.json = lambda: {
            "videos": [video],
            "total": 1
        }
        mock_media.return_value.status_code = 200

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

        respuesta = {
            "autor": {
                "usuario_id": 1234,
                "email": "test@test.com",
                "nombre": None,
                "apellido": None,
                "foto": "url/foto"
            },
            "videos": [video_response],
        }

        response = self.app.get('/usuario/1234/video')

        self.assertEqual(200, response.status_code)
        self.assertEqual(respuesta, response.json)

if __name__ == '__main__':
    unittest.main()
