# pylint: skip-file

import base64
import unittest
from unittest import TestCase

import mock
from mock import MagicMock

from app.servicios.servicio_notificaciones.backend_firebase import BackendFirebase

class BackendFirebaseTestCase(TestCase):
    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    def test_inicializa_firebase_correctamente(self, mock_init, mock_db, mock_cred):
        app = mock_init.return_value = MagicMock()
        BackendFirebase(
            MagicMock(), # log
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'firebase.com',
            'app-server-test',
            'notificaciones'
        )
        mock_cred.assert_called_with({"test": True})
        mock_init.assert_called_with(mock_cred({"test": True}),
                                     {"databaseURL": "firebase.com"},
                                     name='chotuve-notificaciones')
        mock_db.assert_called_with('/app-server-test/notificaciones', app=app)

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    def test_inicializa_firebase_correctamente_sin_raiz(self, mock_init, mock_db, mock_cred):
        app = mock_init.return_value = MagicMock()
        BackendFirebase(
            MagicMock(), # log
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'firebase.com',
            '',
            'notificaciones'
        )
        mock_cred.assert_called_with({"test": True})
        mock_init.assert_called_with(mock_cred({"test": True}),
                                     {"databaseURL": "firebase.com"},
                                     name='chotuve-notificaciones')
        mock_db.assert_called_with('/notificaciones', app=app)

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    @mock.patch('firebase_admin.messaging.send')
    @mock.patch('firebase_admin.messaging.Message')
    @mock.patch('firebase_admin.messaging.Notification')
    def test_envia_notificacion_a_firebase(self, noti, msg, fcm, init, db, _):
        app = init.return_value = MagicMock()
        mock_msg = msg.return_value
        mock_noti = noti.return_value
        nodo_notis = MagicMock()
        nodo_uid = MagicMock()
        nodo_notis.child.return_value = nodo_uid
        nodo_uid.get.return_value = 'token-para-uid-123'
        db.return_value = nodo_notis

        notificador = BackendFirebase(
            MagicMock(), # log
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'firebase.com',
            'app-server-test',
            'notificaciones'
        )

        titulo = 'notificacion de prueba'
        cuerpo = 'cuerpo de la notificacion de prueba'

        notificador.notificar(titulo, cuerpo, 123)

        nodo_notis.child.assert_called_with("123")
        nodo_uid.get.assert_called_once()
        noti.assert_called_with(
            title=titulo,
            body=cuerpo
        )
        msg.assert_called_with(
            notification=mock_noti,
            token='token-para-uid-123'
        )
        fcm.assert_called_with(mock_msg, app=app)

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.db.reference')
    @mock.patch('firebase_admin.initialize_app')
    @mock.patch('firebase_admin.messaging.send')
    def test_no_envia_notificacion_si_no_hay_token(self, fcm, init, db, _):
        app = init.return_value = MagicMock()
        nodo_notis = MagicMock()
        nodo_uid = MagicMock()
        nodo_notis.child.return_value = nodo_uid
        nodo_uid.get.return_value = None
        db.return_value = nodo_notis

        notificador = BackendFirebase(
            MagicMock(), # log
            str(base64.encodebytes(b'{"test": true}'), 'utf-8'),
            'firebase.com',
            'app-server-test',
            'notificaciones'
        )

        titulo = 'notificacion de prueba'
        cuerpo = 'cuerpo de la notificacion de prueba'

        notificador.notificar(titulo, cuerpo, 123)

        nodo_notis.child.assert_called_with("123")
        nodo_uid.get.assert_called_once()
        fcm.assert_not_called()

if __name__ == '__main__':
    unittest.main()
