import unittest

from tests.base import BaseTestCase

class AppTestCase(BaseTestCase):
    def test_devuelve_200(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})


if __name__ == '__main__':
    unittest.main()
