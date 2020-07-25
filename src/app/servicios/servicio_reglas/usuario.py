
class Usuario:
    def __init__(self, usuario):
        self.cantidad_contactos = usuario.get('cantidad-contactos', 0)
