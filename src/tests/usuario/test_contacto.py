import unittest
import mock

from tests.base import LoginMockTestCase

class ContactoTestCase(LoginMockTestCase):
    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    def test_get_mis_contactos_devuelve_vacio_sin_contactos(self, mock_auth):
        mock_auth.return_value = {}
        response = self.app.get('/usuario/contacto')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    @mock.patch('app.models.contacto.Contacto.obtener_contactos')
    def test_get_mis_contactos_devuelve_contactos(self, mock_contacto, mock_auth):
        mock_auth.return_value = {1: {'id': 1, 'email': 'test@test.com', 'foto': 'url'}}
        mock_contacto.return_value = [1]

        response = self.app.get('/usuario/contacto')

        mock_contacto.assert_called_with(1)

        self.assertEqual(200, response.status_code)
        self.assertEqual([{'id': 1, 'email': 'test@test.com', 'foto': 'url'}], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    def test_get_contactos_de_otro_devuelve_vacio_sin_contactos(self, mock_auth):
        mock_auth.return_value = {}
        response = self.app.get('/usuario/2/contacto')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    @mock.patch('app.servicios.auth_server.obtener_usuarios')
    @mock.patch('app.models.contacto.Contacto.obtener_contactos')
    def test_get_contactos_de_otro_devuelve_contactos(self, mock_contacto, mock_auth):
        mock_auth.return_value = {1: {'id': 1, 'email': 'test@test.com', 'foto': 'url'}}
        mock_contacto.return_value = [1]

        response = self.app.get('/usuario/2/contacto')

        mock_contacto.assert_called_with(2)

        self.assertEqual(200, response.status_code)
        self.assertEqual([{'id': 1, 'email': 'test@test.com', 'foto': 'url'}], response.json)


if __name__ == '__main__':
    unittest.main()
