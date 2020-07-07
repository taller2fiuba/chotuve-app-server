import unittest

from tests.base import BaseTestCase
from app.servicios.servicio_chat import ChatNulo

class ChatNuloTestCase(BaseTestCase):
    def test_permite_enviar_mensaje(self):
        chat = ChatNulo()
        self.assertTrue(hasattr(chat, 'enviar_mensaje'))
        chat.enviar_mensaje('hola', 1, 2)

if __name__ == '__main__':
    unittest.main()
