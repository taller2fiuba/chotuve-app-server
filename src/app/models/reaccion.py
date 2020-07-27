# pylint: skip-file
import enum
from sqlalchemy import func
from app import db

class TipoReaccion(enum.Enum):
    NO_ME_GUSTA = 'NO_ME_GUSTA'
    ME_GUSTA = 'ME_GUSTA'

class Reaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video = db.Column(db.String(32))
    usuario = db.Column(db.Integer)
    tipo = db.Column(db.Enum(TipoReaccion))

    @staticmethod
    def contar_reacciones(video, tipo):
        return Reaccion.query.filter_by(video=video, tipo=tipo).count()

    @staticmethod
    def obtener_reaccion(video, usuario):
        reaccion = Reaccion.query.filter_by(video=video, usuario=usuario).one_or_none()
        if reaccion:
            return reaccion.tipo
        return None

    @staticmethod
    def cantidad_reacciones():
        return Reaccion.query.count()
