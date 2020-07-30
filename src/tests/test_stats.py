import unittest
import mock

from tests.base import BaseTestCase

class StatsTestCase(BaseTestCase):
    @mock.patch('app.models.comentario.Comentario.query')
    @mock.patch('app.models.reaccion.Reaccion.query')
    def test_cantidad_de_contactos(self, mock_db_c, mock_db_r):
        mock_db_c.count.return_value = 0
        mock_db_r.count.return_value = 0

        response = self.app.get('/stats/historico')
        estadisticas = response.json
        self.assertEqual(estadisticas["total_comentarios"], 0)
        self.assertEqual(estadisticas["total_reacciones"], 0)

if __name__ == '__main__':
    unittest.main()
