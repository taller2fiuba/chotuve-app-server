import unittest
from unittest import TestCase

from mock import MagicMock

from app.servicios.servicio_notificaciones.notificador_texto_plano import NotificadorTextoPlano

REMITENTE = {
    "id": 123,
    "nombre": "Remitente Test",
    "email": "remitente@test.com"
}

DESTINATARIO = {
    "id": 321,
    "nombre": "Destinatario Test",
    "email": "destinatario@test.com"
}

VIDEO = {
    "_id": "asdasd213123",
    "usuario_id": DESTINATARIO["id"],
    "titulo": "Video Test"
}

class NotificadorTextoPlanoTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.mock_backend = MagicMock(notificar=MagicMock())
        self.notificador = NotificadorTextoPlano(self.mock_backend)

    def test_enviar_solicitud_contacto(self):
        self.notificador.enviar_solicitud_contacto(REMITENTE, DESTINATARIO)
        self.mock_backend.notificar.assert_called_with(
            'Nueva solicitud de contacto.',
            f'{REMITENTE["nombre"]} te envió una solicitud de contacto.',
            DESTINATARIO["id"]
        )

    def test_aceptar_solicitud_contacto(self):
        self.notificador.aceptar_solicitud_contacto(REMITENTE, DESTINATARIO)
        self.mock_backend.notificar.assert_called_with(
            'Solicitud de contacto aceptada.',
            f'Ahora vos y {REMITENTE["nombre"]} son contactos.',
            DESTINATARIO["id"]
        )

    def test_enviar_mensaje_chat(self):
        self.notificador.enviar_mensaje_chat('mensaje', REMITENTE, DESTINATARIO)
        self.mock_backend.notificar.assert_called_with(
            f'Nuevo mensaje de {REMITENTE["nombre"]}.',
            'mensaje',
            DESTINATARIO["id"]
        )

    def test_reaccionar_me_gusta_video(self):
        self.notificador.reaccionar_me_gusta_video(VIDEO, REMITENTE)
        self.mock_backend.notificar.assert_called_with(
            'Nueva reacción a tu video',
            f'A {REMITENTE["nombre"]} le gustó tu video {VIDEO["titulo"]}.',
            VIDEO["usuario_id"]
        )

    def test_comentar_video(self):
        self.notificador.comentar_video('comentario', VIDEO, REMITENTE)
        self.mock_backend.notificar.assert_called_with(
            f'{REMITENTE["nombre"]} comentó tu video',
            'comentario',
            VIDEO["usuario_id"]
        )


if __name__ == '__main__':
    unittest.main()
