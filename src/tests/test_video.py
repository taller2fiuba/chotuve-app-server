import unittest
import mock

from app import app


class VideoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @mock.patch('app.resources.video.requests.post')
    def test_post_agregar_video(self, mock_post):
        mock_post.return_value.json = lambda: {}
        mock_post.return_value.status_code = 200
        response = self.app.post('/video', json={
            'url': 'value', 'titulo': 'data'})
        self.assertEqual({}, response.json)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
