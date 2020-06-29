# pylint: skip-file
import enum
from sqlalchemy import func
from app import db

class SolicitudContacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_emisor = db.Column(db.Integer)
    usuario_receptor = db.Column(db.Integer)

    @staticmethod
    def obtener_solicitudes_pendientes(usuario_id):
        '''
        Devuelve un iterable con todas las solicitudes pendientes del usuario.
        '''
        return SolicitudContacto.query.filter_by(usuario_receptor=usuario_id).all()

    @staticmethod
    def hay_solicitud(usuario_emisor, usuario_receptor):
        '''
        Devuelve True si hay una solicitud pendiente del usuario emisor
        al usuario receptor.
        '''
        return SolicitudContacto.query.\
                    filter_by(usuario_emisor=usuario_emisor,
                              usuario_receptor=usuario_receptor).one_or_none()