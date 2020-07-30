# pylint: skip-file
import enum
from sqlalchemy import func
from app import db
from datetime import timedelta, date

class TipoReaccion(enum.Enum):
    NO_ME_GUSTA = 'NO_ME_GUSTA'
    ME_GUSTA = 'ME_GUSTA'

class Reaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video = db.Column(db.String(32))
    usuario = db.Column(db.Integer)
    tipo = db.Column(db.Enum(TipoReaccion))
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())

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

    @staticmethod
    def reacciones_por_fecha(f_inicio, f_final):
        query = db.session.query(db.func.date(Reaccion.fecha), db.func.count('*')).filter(Reaccion.fecha >= f_inicio,
               Reaccion.fecha <= f_final).group_by(db.func.date(Reaccion.fecha)).all()
        reacciones = {}
        for fecha in query:
            reacciones[str(fecha[0])] = fecha[1]
        
        #saco los segundos y minutos 
        fecha = date(f_inicio.year, f_inicio.month, f_inicio.day)
        f_final = date(f_final.year, f_final.month, f_final.day)
        while fecha <= f_final:
            if str(fecha) not in reacciones:
                reacciones[str(fecha)] = 0
            fecha = fecha + timedelta(days=1)
        return reacciones
