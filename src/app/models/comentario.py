# pylint: skip-file
from app import db
from sqlalchemy import func
from datetime import timedelta, date

MAX_LEN_COMENTARIO = 5000

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video = db.Column(db.String(32))
    usuario = db.Column(db.Integer)
    comentario = db.Column(db.String(MAX_LEN_COMENTARIO))
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def contar_comentarios(video_id):
        return Comentario.query.filter_by(video=video_id).count()
    
    @staticmethod
    def cantidad_comentarios():
        return Comentario.query.count()

    @staticmethod
    def comentarios_por_fecha(f_inicio, f_final):
        f_final = f_final + timedelta(days=1) #este es ya que sino la query se hara para la f_final
                                              #a las 00 y no entraran las comentarios de f_final
        query = db.session.query(db.func.date(Comentario.fecha), db.func.count('*')).\
                                 filter(Comentario.fecha >= f_inicio,Comentario.fecha <= f_final).\
                                 group_by(db.func.date(Comentario.fecha)).all()
        comentarios = {}
        for fecha in query:
            comentarios[str(fecha[0])] = fecha[1]
        
        #saco los segundos y minutos
        fecha = date(f_inicio.year, f_inicio.month, f_inicio.day)
        f_final = date(f_final.year, f_final.month, f_final.day)
        while fecha <= f_final:
            if str(fecha) not in comentarios:
                comentarios[str(fecha)] = 0
            fecha = fecha + timedelta(days=1)
        return comentarios
