from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC

class AccionesVideo(BaseActions):
    def __init__(self, video):
        self.video = video

    @rule_action(params={"cantidad": FIELD_NUMERIC})
    def incrementar_importancia(self, cantidad):
        self.video.importancia += cantidad

    @rule_action(params={"cantidad": FIELD_NUMERIC})
    def decrementar_importancia(self, cantidad):
        self.video.importancia -= cantidad
