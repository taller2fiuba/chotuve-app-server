import unittest
import mock

from tests.base import LoginMockTestCase
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class VideoTestCase(LoginMockTestCase):
    @mock.patch('media_server_api.requests.post')
    def test_post_agregar_video(self, mock_post):
        mock_post.return_value.json = lambda: {}
        mock_post.return_value.status_code = 201
        body = {
            'url': 'value',
            'titulo': 'data',
            'descripcion': 'descripcion',
            'ubicacion': 'mi casa',
            'duracion': 0,
            'visibilidad': 'publico',
        }

        response = self.app.post('/video', json=body)

        body['usuario_id'] = 1 # agregar usuario por defecto
        mock_post.assert_called_with(f'{CHOTUVE_MEDIA_URL}/video', json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual({}, response.json)

    @mock.patch('media_server_api.requests.post')
    def test_post_agregar_video_sin_visibilidad(self, mock_post):
        mock_post.return_value.json = lambda: {}
        mock_post.return_value.status_code = 201
        body = {
            'url': 'value',
            'titulo': 'data',
            'descripcion': 'descripcion',
            'ubicacion': 'mi casa',
            'duracion': 60,
        }

        response = self.app.post('/video', json=body)

        body['usuario_id'] = 1 # agregar usuario por defecto
        body['visibilidad'] = 'publico' # agrega visibilidad por defecto
        mock_post.assert_called_with(f'{CHOTUVE_MEDIA_URL}/video', json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('media_server_api.obtener_videos')
    def test_obtener_videos_sin_parametros(self, mock_obtener_videos, mock_obtener_usuarios):

        mock_obtener_videos.return_value.json = lambda: {
            "videos": [],
            "total": 0
        }
        mock_obtener_videos.return_value.status_code = 200
        mock_obtener_usuarios.return_value.json = lambda: []
        mock_obtener_usuarios.return_value.status_code = 200

        response = self.app.get('/video')

        mock_obtener_videos.assert_called_with({'offset': 0, 'cantidad': 10, 'contactos': []})
        mock_obtener_usuarios.assert_called_with({'ids':'', 'offset': 0, 'cantidad': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('media_server_api.obtener_videos')
    def test_obtener_videos_con_parametros(self, mock_obtener_videos, mock_obtener_usuarios):
        mock_obtener_videos.return_value.json = lambda: {
            "videos": [],
            "total": 0
        }
        mock_obtener_videos.return_value.status_code = 200
        mock_obtener_usuarios.return_value.json = lambda: []
        mock_obtener_usuarios.return_value.status_code = 200
        offset = 10
        cantidad = 5

        response = self.app.get(f'/video?offset={offset}&cantidad={cantidad}')

        mock_obtener_videos.assert_called_with({
            'offset': offset, 'cantidad': cantidad, 'contactos': []
        })
        mock_obtener_usuarios.assert_called_with({'ids':'', 'offset': offset, 'cantidad': cantidad})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('media_server_api.obtener_videos')
    def test_obtener_videos_correcto(self, mock_obtener_videos, mock_obtener_usuarios):
        mock_obtener_videos.return_value.status_code = 200
        mock_obtener_videos.return_value.json = lambda: {
            "videos": [
                {
                    '_id':'c78',
                    'url': '/test/video.mp4',
                    'titulo': 'mi video',
                    'duracion': 600,
                    'time_stamp': '2019-07-02',
                    'visibilidad': 'publico',
                    'usuario_id': 123,
                    'descripcion': 'una descripción'
                }
            ],
            "total": 1
        }

        mock_obtener_usuarios.return_value.status_code = 200
        mock_obtener_usuarios.return_value.json = lambda: [
            {
                'id': 123,
                'nombre': 'autor_test',
                'apellido': 'apellido_test',
                'email': 'email@test',
                'foto': 'foto.jpg'
            }
        ]

        response = self.app.get(f'/video')

        valor_esperado = [
            {
                'autor': {
                    'usuario_id': 123,
                    'email': 'email@test',
                    'apellido': 'apellido_test',
                    'nombre': 'autor_test',
                    'foto': 'foto.jpg'
                },
                'creacion': '2019-07-02',
                'descripcion': 'una descripción',
                'duracion': 600,
                'id': 'c78',
                'titulo': 'mi video',
                'url': '/test/video.mp4',
                'visibilidad': 'publico',
                'no-me-gustas': 0,
                'me-gustas': 0,
                'mi-reaccion': None,
                'cantidad-comentarios': 0
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(valor_esperado, response.json)

    @mock.patch('media_server_api.obtener_videos')
    def test_obtener_videos_falla(self, mock_obtener_videos):
        mock_obtener_videos.return_value.json = lambda: {}
        mock_obtener_videos.return_value.status_code = 400

        response = self.app.get(f'/video')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.obtener_usuarios')
    @mock.patch('media_server_api.obtener_videos')
    def test_obtener_videos_falla_porque_no_se_pudo_obtener_usuarios(self,
                                                                     mock_obtener_videos,
                                                                     mock_obtener_usuarios):
        mock_obtener_videos.return_value.json = lambda: {
            "videos": [],
            "total": 0
        }
        mock_obtener_videos.return_value.status_code = 200
        mock_obtener_usuarios.return_value.json = lambda: {}
        mock_obtener_usuarios.return_value.status_code = 400

        response = self.app.get(f'/video')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_video')
    def test_obtener_video_correcto(self, mock_obtener_video, mock_get_usuario):
        mock_obtener_video.return_value.status_code = 200
        mock_obtener_video.return_value.json = lambda: {
            '_id':'1loR8g7',
            'url': '/test/video.mp4',
            'titulo': 'mi video',
            'duracion': 600,
            'time_stamp': '2019-07-02',
            'visibilidad': 'publico',
            'usuario_id': 456,
            'descripcion': 'una descripción'
        }

        mock_get_usuario.return_value.status_code = 200
        mock_get_usuario.return_value.json = lambda: {
            'id': 456,
            'nombre': 'autor_test',
            'apellido': 'apellido_test',
            'email': 'email@test',
            'foto': 'foto.jpg'
        }

        response = self.app.get(f'/video/1loR8g7')

        valor_esperado = {
            'autor': {
                'usuario_id': 456,
                'email': 'email@test',
                'apellido': 'apellido_test',
                'nombre': 'autor_test',
                'foto': 'foto.jpg'
            },
            'creacion': '2019-07-02',
            'duracion': 600,
            'id': '1loR8g7',
            'titulo': 'mi video',
            'url': '/test/video.mp4',
            'visibilidad': 'publico',
            'descripcion': 'una descripción',
            'no-me-gustas': 0,
            'me-gustas': 0,
            'mi-reaccion': None,
            'cantidad-comentarios': 0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(valor_esperado, response.json)

    @mock.patch('media_server_api.obtener_video')
    def test_obtener_video_falla_porque_no_existe_id(self, mock_obtener_video):
        mock_obtener_video.return_value.json = lambda: {}
        mock_obtener_video.return_value.status_code = 404

        response = self.app.get(f'/video/13grt5')

        self.assertEqual(response.status_code, 404)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.get_usuario')
    @mock.patch('media_server_api.obtener_video')
    def test_obtener_video_falla_porque_no_existe_usuario(self,
                                                          mock_obtener_video,
                                                          mock_get_usuario):
        mock_obtener_video.return_value.json = lambda: {'usuario_id': 12}
        mock_obtener_video.return_value.status_code = 200
        mock_get_usuario.return_value.json = lambda: {}
        mock_get_usuario.return_value.status_code = 400

        response = self.app.get(f'/video/13grt5')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()
