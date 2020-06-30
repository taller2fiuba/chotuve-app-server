import unittest
import mock

from app.models.solicitud_contacto import SolicitudContacto

class SolicitudContactoTestCase(unittest.TestCase):
    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.query')
    def test_obtener_solicitudes_pendientes_devuelve_solicitudes(self, mock_db):
        recibida = SolicitudContacto(id=2, usuario_emisor=3, usuario_receptor=1)

        mock_db.filter_by.return_value.all.return_value = [
            recibida
        ]

        recibidas = SolicitudContacto.obtener_solicitudes_pendientes(1)

        self.assertEqual(1, len(recibidas))
        self.assertEqual(recibida, recibidas[0])

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.query')
    def test_hay_solicitud_devuelve_la_solicitud_si_hay(self, mock_db):
        solicitud = SolicitudContacto(id=2, usuario_emisor=3, usuario_receptor=1)

        mock_db.filter_by.return_value.one_or_none.return_value = solicitud

        recibida = SolicitudContacto.hay_solicitud(3, 1)

        self.assertEqual(solicitud, recibida)

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.query')
    def test_hay_solicitud_devuelve_none_si_no_hay(self, mock_db):
        mock_db.filter_by.return_value.one_or_none.return_value = None

        recibida = SolicitudContacto.hay_solicitud(3, 1)

        self.assertIsNone(recibida)

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.query')
    def test_obtener_por_id_devuelve_solicitud(self, mock_db):
        mock_db.filter_by.return_value.one_or_none.return_value = \
            SolicitudContacto(id=1, usuario_emisor=1, usuario_receptor=2)

        self.assertIsNotNone(SolicitudContacto.obtener_por_id(1))

    @mock.patch('app.models.solicitud_contacto.SolicitudContacto.query')
    def test_obtener_por_id_devuelve_none_si_no_hay_solicitud(self, mock_db):
        mock_db.filter_by.return_value.one_or_none.return_value = None

        self.assertIsNone(SolicitudContacto.obtener_por_id(1))

if __name__ == '__main__':
    unittest.main()
