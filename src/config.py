#!/usr/bin/env python3
#pylint: skip-file

import os
from logging.config import dictConfig

def blow(envvar):
    '''
    Lanza una excepción indicando que una variable de entorno requerida no esta
    configurada o tiene un valor incorrecto.
    '''
    valor = os.environ.get(envvar)
    raise ValueError(f'La variable de entorno {envvar} tiene un ' +
                     'valor incorrecto: ' + repr(valor))

def configurar_logger():
    dictConfig(dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            "default": {"format": "%(levelname)s en %(module)s: %(message)s"},
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        root={"handlers": ["console"], "level": "INFO"},
    ))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or blow('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHOTUVE_MEDIA_URL = os.environ.get('CHOTUVE_MEDIA_URL') or "http://localhost:27080"
    CHOTUVE_AUTH_URL = os.environ.get('CHOTUVE_AUTH_URL') or "http://localhost:26080"
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    FIREBASE_CREDENCIALES = os.environ.get('FIREBASE_CREDENCIALES')
    FIREBASE_CHAT_DB_URL = os.environ.get('FIREBASE_CHAT_DB_URL') or "https://chotuve-a8587.firebaseio.com/"
    FIREBASE_CHAT_DB_RAIZ = os.environ.get('FIREBASE_CHAT_DB_RAIZ') or "app-server-dev"
    FIREBASE_CHAT_DB_RECURSO_CHATS = os.environ.get('FIREBASE_CHAT_DB_RECURSO_CHATS') or "chats"
    FIREBASE_CHAT_DB_RECURSO_MENSAJES = os.environ.get('FIREBASE_CHAT_DB_RECURSO_MENSAJES') or "mensajes"
    APP_SERVER_TOKEN = os.environ.get('APP_SERVER_TOKEN')
    APP_VERSION = "0.0.1"
