from .interfaz_backend import InterfazBackend

class BackendLogger(InterfazBackend): # pragma: no cover
    def __init__(self, log):
        self.log = log

    def notificar(self, titulo: str, cuerpo: str, usuario_id: int):
        self.log.info(f'[NOTIF para {usuario_id}] ({titulo}) {cuerpo}')
