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

    @mock.patch('media_server_api.get_videos')
    def test_get_videos_sin_parametros_se_envia_con_parametros_por_defecto(self, mock_get_videos):
        mock_get_videos.return_value.json = lambda: []
        mock_get_videos.return_value.status_code = 200

        response = self.app.get('/video')

        params = {'offset': 0, 'cantidad': 10}
        mock_get_videos.assert_called_with(params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

    @mock.patch('media_server_api.get_videos')
    def test_get_videos_con_parametros(self, mock_get_videos):
        mock_get_videos.return_value.json = lambda: []
        mock_get_videos.return_value.status_code = 200

        response = self.app.get('/video?offset=10&cantidad=5')

        params = {'offset': 10, 'cantidad': 5}
        mock_get_videos.assert_called_with(params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json)

if __name__ == '__main__':
    unittest.main()
