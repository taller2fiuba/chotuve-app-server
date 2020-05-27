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
            'duracion': 0,
        }

        response = self.app.post('/video', json=body)

        body['usuario_id'] = 1 # agregar usuario por defecto
        body['visibilidad'] = 'publico'
        mock_post.assert_called_with(f'{CHOTUVE_MEDIA_URL}/video', json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()
