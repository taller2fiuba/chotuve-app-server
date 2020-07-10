# pylint: skip-file
'''
Localizador de servicios

Este paquete implementa un localizador de servicios en base a la configuración
de la aplicación.

Los servicios exportados por este paquete serán configurados automáticamente
durante el inicio de la aplicación.
'''

# Servicios exportados
auth_server = None
chat = None

def configurar_servicios(app):
    '''
    Inicializa y exporta los servicios configurados.
    '''
    _configurar_auth_server(app)
    _configurar_chat(app)

def _configurar_auth_server(app):
    global auth_server
    from .servicio_auth_server import AuthServer
    auth_server = AuthServer(app.config.get('CHOTUVE_AUTH_URL'))

def _configurar_chat(app):
    global chat

    if app.config.get('FIREBASE_CREDENCIALES'):
        from .servicio_chat.chat_firebase import ChatFirebase
        chat = ChatFirebase(
            app.config.get('FIREBASE_CREDENCIALES'),
            app.config.get('FIREBASE_CHAT_DB_URL'),
            app.config.get('FIREBASE_CHAT_DB_RAIZ'),
            app.config.get('FIREBASE_CHAT_DB_RECURSO_CHATS'),
            app.config.get('FIREBASE_CHAT_DB_RECURSO_MENSAJES')
        )
    else:
        from .servicio_chat.chat_nulo import ChatNulo
        chat = ChatNulo()
