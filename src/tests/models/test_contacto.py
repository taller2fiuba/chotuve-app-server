import unittest
import mock

from app.models.contacto import Contacto

class ContactoTestCase(unittest.TestCase):
    @mock.patch('app.models.contacto.Contacto.query')
    def test_obtener_contactos_ignora_el_sentido(self, mock_db):
        mock_db.filter.return_value.all.return_value = [
            Contacto(id=1, usuario_1=1, usuario_2=2),
            Contacto(id=2, usuario_1=3, usuario_2=1)
        ]

        contactos = Contacto.obtener_contactos(1)

        self.assertEqual([2, 3], contactos)

    @mock.patch('app.models.contacto.Contacto.query')
    def test_contar_contactos_devuelve_cantidad_correcta(self, mock_db):
        mock_db.filter.return_value.all.return_value = [
            Contacto(id=1, usuario_1=1, usuario_2=2),
            Contacto(id=2, usuario_1=3, usuario_2=1)
        ]

        contactos = Contacto.obtener_cantidad_contactos(1)

        self.assertEqual(2, contactos)

    @mock.patch('app.models.contacto.Contacto.query')
    def test_es_contacto_ignora_el_sentido(self, mock_db):
        mock_db.filter.return_value.all.return_value = [
            Contacto(id=1, usuario_1=1, usuario_2=2)
        ]

        self.assertTrue(Contacto.es_contacto(1, 2))
        self.assertTrue(Contacto.es_contacto(2, 1))


if __name__ == '__main__':
    unittest.main()
