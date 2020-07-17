from .interfaz_notificador import InterfazNotificador

class NotificadorNulo(InterfazNotificador): # pragma: no cover
    def __init__(self, log):
        self.log = log

    def enviar_solicitud_contacto(self, remitente: int, destinatario: int):
        self.log.info('[NOTIFICACION] %r envió solicitud de contacto a %r',
                      remitente,
                      destinatario)

    def aceptar_solicitud_contacto(self, remitente: int, destinatario: int):
        self.log.info('[NOTIFICACION] %r aceptó la solictud de %r',
                      remitente,
                      destinatario)

    def enviar_mensaje_chat(self, mensaje: str, remitente: int, destinatario: int):
        self.log.info('[NOTIFICACION] %r envió el mensaje %r a %r',
                      remitente,
                      mensaje,
                      destinatario)

    def reaccionar_me_gusta_video(self, video: dict, remitente: int):
        self.log.info('[NOTIFICACION] %r reaccionó me gusta al video %r de %r',
                      remitente,
                      video.get('_id'),
                      video.get('usuario_id'))

    def comentar_video(self, comentario: str, video: dict, remitente: int):
        self.log.info('[NOTIFICACION] %r comentó %r al video %r de %r',
                      remitente,
                      comentario,
                      video.get('_id'),
                      video.get('usuario_id'))
