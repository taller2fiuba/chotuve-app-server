from abc import abstractmethod

class InterfazChat: # pragma: no cover
    @abstractmethod
    def enviar_mensaje(self, mensaje, remitente, destinatario):
        '''
        Envía un mensaje de chat del remitent al destinatario.

        mensaje: Texto del mensaje a enviar
        remitente: ID del usuario que envía el mensaje
        destinatario: ID del usuario que recibirá el mensaje
        '''
        raise NotImplementedError
