from .interfaz_chat import InterfazChat

class ChatNulo(InterfazChat):
    '''
    Implementación del servicio Chat nula.

    Esta implementación no envía ningún chat.
    '''

    def enviar_mensaje(self, mensaje, remitente, destinatario):
        pass
