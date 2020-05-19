from flask import g

def set_usuario_actual(usuario_actual):
    g.usuario_actual = usuario_actual

def get_usuario_actual():
    return g.usuario_actual
