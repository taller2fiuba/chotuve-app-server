from business_rules.variables import (BaseVariables,
                                      numeric_rule_variable,
                                      string_rule_variable)

class VariablesVideo(BaseVariables):
    def __init__(self, video):
        self.video = video

    @numeric_rule_variable
    def videos_subidos_por_dia(self):
        return self.video.autor.videos_por_dia

    @numeric_rule_variable
    def cantidad_contactos(self):
        return self.video.autor.cantidad_contactos

    @numeric_rule_variable
    def fecha_publicacion(self):
        return self.video.fecha_publicacion

    @numeric_rule_variable
    def cantidad_comentarios(self):
        return self.video.cantidad_comentarios

    @numeric_rule_variable
    def cantidad_reacciones(self):
        return self.video.cantidad_reacciones

    @string_rule_variable
    def ubicacion(self):
        return self.video.ubicacion
