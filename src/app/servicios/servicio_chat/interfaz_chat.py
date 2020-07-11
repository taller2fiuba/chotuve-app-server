from abc import abstractmethod

class InterfazChat:
    @abstractmethod
    def enviar_mensaje(self, mensaje, remitente, destinatario):
        raise NotImplementedError
