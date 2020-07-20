import abc

class InterfazBackend: # pragma: no cover
    @abc.abstractmethod
    def notificar(self, titulo: str, cuerpo: str, usuario_id: int):
        '''
        Emite una notificación de texto plano al usuario indicado.

        titulo: Título a mostrar en la notificación.
        cuerpo: Texto del cuerpo de la notificación.
        usuario_id: ID del usuario que recibirá la notificación.

        Devuelve True si el usuario tiene un dispositivo registrado para
        notificaciones, o False en caso contrario.
        Que el método devuelva True no asegura que la notificación llegue,
        sólo asegura que fue despachada.
        '''
        raise NotImplementedError
