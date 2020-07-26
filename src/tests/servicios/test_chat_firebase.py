import base64
import unittest
from unittest import TestCase

import mock
from mock import MagicMock

from app.servicios.servicio_chat.chat_firebase import ChatFirebase

class ChatFirebaseTestCase(TestCase):
    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    def test_inicializa_firebase_correctamente(self, mock_init, mock_db, mock_cred):
        ChatFirebase(
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'db-url',
            'raiz',
            'chats',
            'mensajes'
        )
        mock_cred.assert_called_with({"test": True})
        mock_init.assert_called_with(mock_cred({"test": True}),
                                     {"databaseURL": "db-url"},
                                     name='chotuve-chat')
        app = mock_init.return_value
        mock_db.assert_has_calls([mock.call('/raiz/chats', app=app),
                                  mock.call('/raiz/mensajes', app=app)])

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    def test_inicializa_firebase_correctamente_sin_raiz(self, mock_init, mock_db, mock_cred):
        ChatFirebase(
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'db-url',
            '',
            'chats',
            'mensajes'
        )
        mock_cred.assert_called_with({"test": True})
        mock_init.assert_called_with(mock_cred({"test": True}),
                                     {"databaseURL": "db-url"},
                                     name='chotuve-chat')
        app = mock_init.return_value
        mock_db.assert_has_calls([mock.call('/chats', app=app),
                                  mock.call('/mensajes', app=app)])

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    @mock.patch('datetime.datetime')
    def test_envia_mensaje_a_firebase_con_id_correcto_1_2(self, mock_time, _, __, ___):
        # Estas horrorosas líneas se deben a que no se puede mockear parcialmente
        # un módulo built-in (datetime).
        mock_time.now = MagicMock()
        mock_time.now.return_value = MagicMock()
        mock_time.now.return_value.timestamp.return_value = 12345.123

        chat = ChatFirebase(
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'db-url',
            'raiz',
            'chats',
            'mensajes'
        )

        mensaje_db_data = {
            'enviadoPor': 1,
            'mensaje': 'mensaje',
            'timestamp': 12345
        }

        chat_db_data = {
            'timestamp': -12345,
            'ultimoMensaje': 'mensaje'
        }

        subnodo_chat_1 = MagicMock()
        subnodo_chat_2 = MagicMock()
        nodo_chats = MagicMock()
        nodo_chats.side_effect = lambda x: subnodo_chat_1 if x == '1' else subnodo_chat_2

        chat.db_chats = MagicMock()
        chat.db_chats.child = nodo_chats
        chat.db_mensajes = MagicMock()
        chat.db_mensajes.child.return_value = MagicMock()

        chat.enviar_mensaje('mensaje', 1, 2)

        chat.db_mensajes.child.assert_called_with('1-2')
        chat.db_mensajes.child.return_value.push.assert_called_with(mensaje_db_data)

        nodo_chats.assert_has_calls([mock.call('1'), mock.call('2')], any_order=True)
        subnodo_chat_1.child.assert_called_with('2')
        subnodo_chat_2.child.assert_called_with('1')
        subnodo_chat_1.child.return_value.set.assert_called_with(chat_db_data)
        subnodo_chat_2.child.return_value.set.assert_called_with(chat_db_data)

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    @mock.patch('datetime.datetime')
    def test_envia_mensaje_a_firebase_con_id_correcto_2_1(self, mock_time, _, __, ___):
        # Estas horrorosas líneas se deben a que no se puede mockear parcialmente
        # un módulo built-in (datetime).
        mock_time.now = MagicMock()
        mock_time.now.return_value = MagicMock()
        mock_time.now.return_value.timestamp.return_value = 12345.123

        chat = ChatFirebase(
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'db-url',
            'raiz',
            'chats',
            'mensajes'
        )

        mensaje_db_data = {
            'enviadoPor': 2,
            'mensaje': 'mensaje',
            'timestamp': 12345
        }

        chat_db_data = {
            'timestamp': -12345,
            'ultimoMensaje': 'mensaje'
        }

        subnodo_chat_1 = MagicMock()
        subnodo_chat_2 = MagicMock()
        nodo_chats = MagicMock()
        nodo_chats.side_effect = lambda x: subnodo_chat_1 if x == '1' else subnodo_chat_2

        chat.db_chats = MagicMock()
        chat.db_chats.child = nodo_chats
        chat.db_mensajes = MagicMock()
        chat.db_mensajes.child.return_value = MagicMock()

        chat.enviar_mensaje('mensaje', 2, 1)

        chat.db_mensajes.child.assert_called_with('1-2')
        chat.db_mensajes.child.return_value.push.assert_called_with(mensaje_db_data)

        nodo_chats.assert_has_calls([mock.call('1'), mock.call('2')], any_order=True)
        subnodo_chat_1.child.assert_called_with('2')
        subnodo_chat_2.child.assert_called_with('1')
        subnodo_chat_1.child.return_value.set.assert_called_with(chat_db_data)
        subnodo_chat_2.child.return_value.set.assert_called_with(chat_db_data)

if __name__ == '__main__':
    unittest.main()
