from flask import g

def set_usuario_actual(usuario_actual, es_admin):
    g.usuario_actual = usuario_actual
    g.es_admin = es_admin

def get_usuario_actual():
    return g.usuario_actual
