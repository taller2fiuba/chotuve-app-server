from business_rules.variables import (BaseVariables,
                                      numeric_rule_variable,
                                      string_rule_variable)

class VariablesVideo(BaseVariables):
    def __init__(self, video):
        self.video = video

    @numeric_rule_variable
    def cantidad_contactos(self):
        return self.video.autor.cantidad_contactos

    @string_rule_variable
    def mi_reaccion(self):
        return self.video.mi_reaccion

    @numeric_rule_variable
    def antiguedad(self):
        return self.video.antiguedad

    @numeric_rule_variable
    def cantidad_comentarios(self):
        return self.video.cantidad_comentarios

    @numeric_rule_variable
    def cantidad_me_gusta(self):
        return self.video.cantidad_me_gusta
