import datetime

from .usuario import Usuario

class Video:
    def __init__(self, video):
        self.datos = video

        self.autor = Usuario(video.get('autor'))
        self.cantidad_me_gusta = video.get('me-gustas', 0)
        self.cantidad_comentarios = video.get('cantidad-comentarios', 0)
        self.mi_reaccion = video.get('mi-reaccion', '')
        now = datetime.datetime.now().timestamp()
        self.antiguedad = int(now - video.get('fecha', now))

        self.importancia = 0
