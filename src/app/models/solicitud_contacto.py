from app import db

class SolicitudContacto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_emisor = db.Column(db.Integer)
    usuario_receptor = db.Column(db.Integer)

    def __repr__(self):
        return f'<SolicitudContacto id={self.id} ' + \
               f'emisor={self.usuario_emisor} ' + \
               f'receptor={self.usuario_receptor}>'

    def __eq__(self, otro):
        return self.usuario_emisor == otro.usuario_emisor and \
               self.usuario_receptor == otro.usuario_receptor

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

    @staticmethod
    def obtener_por_id(solicitud_id):
        '''
        Devuelve la solicitud de contacto con el ID indicado.
        Si no se encontró la solicitud devuelve None.
        '''
        return SolicitudContacto.query.filter_by(id=solicitud_id).one_or_none()
