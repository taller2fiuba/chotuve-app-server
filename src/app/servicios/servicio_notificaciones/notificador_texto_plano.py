from .interfaz_notificador import InterfazNotificador
from .interfaz_backend import InterfazBackend

class NotificadorTextoPlano(InterfazNotificador):
    '''
    Notificador de texto plano.

    Traduce acciones notificables en un título y cuerpo de
    texto plano.
    '''

    def __init__(self, backend: InterfazBackend):
        '''
        Crea un nuevo notificador de texto plano.

        backend: Backend que despachará las notificaciones.
        '''
        self.backend = backend

    def enviar_solicitud_contacto(self, remitente: dict, destinatario: dict):
        titulo = 'Nueva solicitud de contacto.'
        cuerpo = f'{self._obtener_nombre(remitente)} te envió una solicitud de contacto.'

        self.backend.notificar(titulo, cuerpo, destinatario['id'])

    def aceptar_solicitud_contacto(self, remitente: dict, destinatario: dict):
        titulo = 'Solicitud de contacto aceptada.'
        cuerpo = f'Ahora vos y {self._obtener_nombre(remitente)} son contactos.'

        self.backend.notificar(titulo, cuerpo, destinatario['id'])

    def enviar_mensaje_chat(self, mensaje: str, remitente: dict, destinatario: dict):
        titulo = f'Nuevo mensaje de {self._obtener_nombre(remitente)}.'

        self.backend.notificar(titulo, mensaje, destinatario['id'])

    def reaccionar_me_gusta_video(self, video: dict, remitente: dict):
        titulo = 'Nueva reacción a tu video'
        cuerpo = f'A {self._obtener_nombre(remitente)} le gustó tu video {video.get("titulo")}.'

        self.backend.notificar(titulo, cuerpo, video.get("usuario_id"))

    def comentar_video(self, comentario: str, video: dict, remitente: dict):
        titulo = f'{self._obtener_nombre(remitente)} comentó tu video'

        self.backend.notificar(titulo, comentario, video.get("usuario_id"))

    def _obtener_nombre(self, usuario: dict) -> str:
        return usuario.get("nombre") or usuario.get("email")
