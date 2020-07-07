import unittest
import mock

from tests.base import BaseTestCase

class ChatTestCase(BaseTestCase):
    @mock.patch('app.servicios.chat.enviar_mensaje')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    def test_chat_devuelve_201_al_enviar_mensaje(self, mock_contacto, mock_auth, mock_chat):
        mock_auth.return_value = {'id': 2}
        mock_contacto.return_value = True
        response = self.app.post('/chat/2', json={'mensaje': 'hola'})
        self.assertEqual(response.status_code, 201)
        mock_chat.assert_called_once()
        mock_chat.assert_called_with('hola', 1, 2)

    @mock.patch('app.servicios.chat.enviar_mensaje')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    def test_chat_devuelve_400_si_no_es_contacto(self, mock_contacto, mock_auth, _):
        mock_auth.return_value = {'id': 2}
        mock_contacto.return_value = False
        response = self.app.post('/chat/2', json={'mensaje': 'hola'})
        self.assertEqual(response.status_code, 400)

    @mock.patch('app.servicios.chat.enviar_mensaje')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    def test_chat_devuelve_400_si_no_hay_mensaje(self, mock_contacto, mock_auth, _):
        mock_auth.return_value = None
        mock_contacto.return_value = False
        response = self.app.post('/chat/2')
        self.assertEqual(response.status_code, 400)
        response = self.app.post('/chat/2', json={})
        self.assertEqual(response.status_code, 400)

    @mock.patch('app.servicios.chat.enviar_mensaje')
    @mock.patch('app.servicios.auth_server.obtener_usuario')
    @mock.patch('app.models.contacto.Contacto.es_contacto')
    def test_chat_devuelve_404_si_destino_no_existe(self, mock_contacto, mock_auth, _):
        mock_auth.return_value = None
        mock_contacto.return_value = False
        response = self.app.post('/chat/2', json={'mensaje': 'hola'})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
