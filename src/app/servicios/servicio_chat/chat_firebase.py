import datetime
import base64
import json
import firebase_admin
from firebase_admin import credentials, db

from .interfaz_chat import InterfazChat

class ChatFirebase(InterfazChat):
    #pylint: disable=too-many-arguments
    def __init__(self, credenciales, db_url, raiz, recurso_chats, recurso_mensajes):
        '''
        Inicializa el servicio de Chat utilizando Firebase RTDB.

        credenciales: str codificada en base64 con el archivo de credenciales
        db_url: URL de la RTDB a utilizar
        raiz: Ruta al nodo raíz
        recurso_chats: Nombre del nodo donde se almacenarán los chats
        recurso_mensajes: Nombre del nodo donde se almacenarán los mensajes

        Ejemplo: raiz=app/server, recurso_chats=chats, recurso_mensajes=mensajes
        La base se estructuraría de la siguiente forma:
        - app
          - server
            - chats
              - <chats>
            - mensajes
              - <mensajes>
        '''
        credenciales = str(credenciales)
        db_url = str(db_url)
        raiz = str(raiz).rstrip('/')
        if raiz:
            raiz += '/'
        recurso_chats = str(recurso_chats)
        recurso_mensajes = str(recurso_mensajes)

        cred = credentials.Certificate(json.loads(
            base64.decodebytes(bytes(credenciales, 'utf-8'))
        ))
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
        self.db_chats = db.reference(f'/{raiz}{recurso_chats}')
        self.db_mensajes = db.reference(f'/{raiz}{recurso_mensajes}')

    def enviar_mensaje(self, mensaje, remitente, destinatario):
        nombre_chat = f'{remitente}-{destinatario}'
        if remitente > destinatario:
            nombre_chat = f'{destinatario}-{remitente}'

        mensaje_db_data = {
            'enviadoPor': remitente,
            'mensaje': mensaje,
            'timestamp': int(datetime.datetime.now().timestamp())
        }

        chat_db_data = {
            'timestamp': -mensaje_db_data['timestamp'],
            'ultimoMensaje': mensaje_db_data['mensaje']
        }

        self.db_mensajes.child(nombre_chat).push(mensaje_db_data)
        self.db_chats.child(str(remitente)).child(str(destinatario)).set(chat_db_data)
        self.db_chats.child(str(destinatario)).child(str(remitente)).set(chat_db_data)
