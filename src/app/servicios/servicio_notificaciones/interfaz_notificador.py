import abc

class InterfazNotificador: # pragma: no cover
    @abc.abstractmethod
    def enviar_solicitud_contacto(self, remitente: dict, destinatario: dict):
        '''
        Emite una notificación de solicitud de contacto al destinatario.

        remitente: Usuario que emitió la solicitud
        destinatario: Usuario que recibirá la solicitud
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def aceptar_solicitud_contacto(self, remitente: dict, destinatario: dict):
        '''
        Emite una notificación indicando que se aceptó una solicitud de contacto.

        remitente: Usuario que aceptó la solicitud
        destinatario: Usuario que recibirá la notificación
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def enviar_mensaje_chat(self, mensaje: str, remitente: dict, destinatario: dict):
        '''
        Emite una notificación de chat al destinatario.

        La notificación contendrá el mensaje enviado al usuario.

        remitente: Usuario que envió el mensaje
        destinatario: Usuario que recibirá el mensaje
        mensaje: Mensaje enviado
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def reaccionar_me_gusta_video(self, video: dict, remitente: dict):
        '''
        Emite una notificación de que hubo una reacción de tipo "Me Gusta" a un video.

        video: Información del video al que se reaccionó
        remitente: Usuario que reaccionó al video
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def comentar_video(self, comentario: str, video: dict, remitente: dict):
        '''
        Emite una notificación de que se agregó un comentario al video.

        comentario: Texto del comnetario
        video: Información del video comentado
        remitente: Usuario que agregó el comentario
        '''
        raise NotImplementedError
