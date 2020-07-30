from datetime import timedelta, date
from sqlalchemy import or_, func

from app import db

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_1 = db.Column(db.Integer)
    usuario_2 = db.Column(db.Integer)
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self): # pragma: no cover
        return f'<Contacto id={self.id} ' + \
               f'usuario_1={self.usuario_1} ' + \
               f'usuario_2={self.usuario_2}>'

    def __eq__(self, otro):
        return self.usuario_1 == otro.usuario_1 and \
               self.usuario_2 == otro.usuario_2

    @staticmethod
    def obtener_contactos(usuario_id):
        '''
        Devuelve una lista con los ID de usuario de cada uno
        de los contactos del usuario indicado.
        '''
        data = Contacto.query.filter(or_(Contacto.usuario_1 == usuario_id,
                                         Contacto.usuario_2 == usuario_id)).all()

        ret = []
        for contacto in data:
            if contacto.usuario_1 == usuario_id:
                ret.append(contacto.usuario_2)
            else:
                ret.append(contacto.usuario_1)
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

    @staticmethod
    def cantidad_contactos():
        '''
        Devuelve la cantidad de usuarios.
        '''
        return Contacto.query.count()

    @staticmethod
    def contactos_por_fecha(f_inicio, f_final):
        query = db.session.query(db.func.date(Contacto.fecha), db.func.count('*')).\
                                 filter(Contacto.fecha >= f_inicio, Contacto.fecha <= f_final).\
                                 group_by(db.func.date(Contacto.fecha)).all()
        contactos = {}
        for fecha in query:
            contactos[str(fecha[0])] = fecha[1]

        #saco los segundos y minutos
        fecha = date(f_inicio.year, f_inicio.month, f_inicio.day)
        f_final = date(f_final.year, f_final.month, f_final.day)
        while fecha <= f_final:
            if str(fecha) not in contactos:
                contactos[str(fecha)] = 0
            fecha = fecha + timedelta(days=1)
        return contactos
