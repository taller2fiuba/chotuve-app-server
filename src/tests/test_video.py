import unittest

from app import app


class VideoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_post_agregar_video(self):
        response = self.app.post('/video', json={
            'url': 'value', 'titulo': 'data'})
        self.assertEqual({'url': 'value', 'titulo': 'data'}, response.json)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
