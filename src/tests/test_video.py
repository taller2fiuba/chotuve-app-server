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

    @mock.patch('auth_server_api.get_usuarios')
    @mock.patch('media_server_api.get_videos')
    def test_get_videos_sin_parametros_se_envia_con_parametros_por_defecto(self,
                                                                           mock_get_videos,
                                                                           mock_get_usuarios):
        mock_get_videos.return_value.json = lambda: []
        mock_get_videos.return_value.status_code = 200
        mock_get_usuarios.return_value.json = lambda: []
        mock_get_usuarios.return_value.status_code = 200

        response = self.app.get('/video')

        mock_get_videos.assert_called_with({'offset': 0, 'cantidad': 10})
        mock_get_usuarios.assert_called_with({'ids':'', 'offset': 0, 'cantidad': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.get_usuarios')
    @mock.patch('media_server_api.get_videos')
    def test_get_videos_con_parametros(self, mock_get_videos, mock_get_usuarios):
        mock_get_videos.return_value.json = lambda: []
        mock_get_videos.return_value.status_code = 200
        mock_get_usuarios.return_value.json = lambda: []
        mock_get_usuarios.return_value.status_code = 200
        offset = 10
        cantidad = 5

        response = self.app.get(f'/video?offset={offset}&cantidad={cantidad}')

        mock_get_videos.assert_called_with({'offset': offset, 'cantidad': cantidad})
        mock_get_usuarios.assert_called_with({'ids':'', 'offset': offset, 'cantidad': cantidad})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('auth_server_api.get_usuarios')
    @mock.patch('media_server_api.get_videos')
    def test_get_videos_correcto(self, mock_get_videos, mock_get_usuarios):
        mock_get_videos.return_value.status_code = 200
        mock_get_videos.return_value.json = lambda: [
            {
                '_id':'c78',
                'url': '/test/video.mp4',
                'titulo': 'mi video',
                'duracion': 600,
                'time_stamp': '2019-07-02',
                'visibilidad': 'publico',
                'usuario_id': 123
            }
        ]

        mock_get_usuarios.return_value.status_code = 200
        mock_get_usuarios.return_value.json = lambda: [
            {
                'id': 123,
                'nombre': 'autor_test',
                'apellido': 'apellido_test',
                'email': 'apellidos_test'
            }
        ]

        response = self.app.get(f'/video')

        valor_esperado = [
            {
                'autor': {
                    'apellido': 'apellido_test',
                    'email': 'apellidos_test',
                    'nombre': 'autor_test',
                    'usuario_id': 123
                },
                'creacion': '2019-07-02',
                'duracion': 600,
                'id': 'c78',
                'titulo': 'mi video',
                'url': '/test/video.mp4',
                'visibilidad': 'publico'
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(valor_esperado, response.json)

    @mock.patch('media_server_api.get_videos')
    def test_get_videos_falla(self, mock_get_videos):
        mock_get_videos.return_value.json = lambda: {}
        mock_get_videos.return_value.status_code = 400

        response = self.app.get(f'/video')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

    @mock.patch('auth_server_api.get_usuarios')
    @mock.patch('media_server_api.get_videos')
    def test_get_usuarios_falla(self, mock_get_videos, mock_get_usuarios):
        mock_get_videos.return_value.json = lambda: []
        mock_get_videos.return_value.status_code = 200
        mock_get_usuarios.return_value.json = lambda: {}
        mock_get_usuarios.return_value.status_code = 400

        response = self.app.get(f'/video')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()
