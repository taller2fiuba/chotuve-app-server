import unittest
import mock

from tests.base import BaseTestCase

class VideoTestCase(BaseTestCase):
    @mock.patch('app.resources.video.requests.post')
    def test_post_agregar_video(self, mock_post):
        mock_post.return_value.json = lambda: {}
        mock_post.return_value.status_code = 200
        response = self.app.post('/video', json={'url': 'value', 'titulo': 'data'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({}, response.json)

if __name__ == '__main__':
    unittest.main()
