# pylint: skip-file
from app import db
from sqlalchemy import func

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
