import base64
import json
import firebase_admin
from firebase_admin import credentials, db, messaging

from .interfaz_backend import InterfazBackend

class BackendFirebase(InterfazBackend):
    # pylint: disable=too-many-arguments
    def __init__(self, log, credenciales, db_url, raiz, recurso_notificaciones):
        '''
        Inicializa el servicio de notificaciones a través de Firebase Cloud
        Messaging.

        Este servicio depende de FCM y de Firebase RealTime Database para
        recuperar los tokens de dispositivo.

        Se espera que la RTDB ubicada en db_url contenga debajo del subarbol
        raiz un nodo llamado recurso_notificaciones donde cada elemento sea
        una asociación de un ID de usuario de Chotuve a un token de
        dispositivo.
        Por ejemplo, si raiz='app/server' y recurso_notificaciones='notis',
        se asume la siguiente estructura de la RTDB:
        - db_url
           - app
              - server
                 - notis
                    - <id>: <token>
                    - <id>: <token>

        credenciales: str, JSON codificado en base64 del archivo de credenciales.
        db_url: str, DB de firebase a utilizar
        raiz: str, raiz del subarbol de tokens
        recurso_notificaciones: str, nombre del recurso de notificaciones
        '''
        self.log = log
        raiz = str(raiz).rstrip('/')
        if raiz:
            raiz += '/'
        credenciales = str(credenciales)
        recurso_notificaciones = str(recurso_notificaciones)
        db_url = str(db_url)

        cred = credentials.Certificate(json.loads(
            base64.decodebytes(bytes(credenciales, 'utf-8'))
        ))
        self.app = firebase_admin.initialize_app(cred,
                                                 {'databaseURL': db_url},
                                                 name='chotuve-notificaciones')
        self.db_tokens = db.reference(f'/{raiz}{recurso_notificaciones}',
                                      app=self.app)

    def notificar(self, titulo: str, cuerpo: str, usuario_id: int):
        '''
        Envía una notificación al dispositivo del usuario.

        Si el usuario no tiene un dispositivo registrado para recibir notificaciones
        no se realizará ninguna acción.
        '''
        token = self._recuperar_token(usuario_id)
        if not token:
            self.log.info('[NotifFirebase] No hay token de dispositivo para %r', usuario_id)
            return False

        response = self._enviar_notificacion(titulo, cuerpo, token)
        self.log.info('[NotifFirebase] Notificación enviada a %r (%r)', usuario_id, response)
        return True

    def _enviar_notificacion(self, titulo: str, cuerpo: str, token: str):
        '''
        Envía una notificación a un determinado token.
        '''
        message = messaging.Message(
            notification=messaging.Notification(
                title=titulo,
                body=cuerpo,
            ),
            token=token
        )

        return messaging.send(message, app=self.app)

    def _recuperar_token(self, usuario_id: int):
        '''
        Recupera el token de un usuario desde la RTDB.

        Devuelve una cadena con el token o None si el usuario no tiene
        el dispositivo registrado.
        '''
        return self.db_tokens.child(str(usuario_id)).get()
