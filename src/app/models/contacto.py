# pylint: skip-file
import enum
from sqlalchemy import or_
from app import db

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_1 = db.Column(db.Integer)
    usuario_2 = db.Column(db.Integer)

    @staticmethod
    def obtener_contactos(usuario_id):
        '''
        Devuelve una lista con los ID de usuario de cada uno
        de los contactos del usuario indicado.
        '''
        data = Contacto.query.filter(or_(Contacto.usuario_1 == usuario_id, 
                                         Contacto.usuario_2 == usuario_id)).all()

        ret = []
        for c in data:
            if c.usuario_1 == usuario_id:
                ret.append(c.usuario_2)
            else:
                ret.append(c.usuario_1)
        
        return ret
    
    @staticmethod
    def obtener_cantidad_contactos(usuario_id):
        '''
        Devuelve la cantidad de contactos que tiene el usuario.
        '''
        return len(Contacto.obtener_contactos(usuario_id))
    
    @staticmethod
    def es_contacto(usuario_id, otro_usuario_id):
        '''
        Devuelve True si otro_usuario es contacto de usuario.
        '''
        return otro_usuario_id in Contacto.obtener_contactos(usuario_id)