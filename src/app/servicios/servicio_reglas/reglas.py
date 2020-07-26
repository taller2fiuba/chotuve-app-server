REGLAS = [
    # comentarios > 2: +2
    {"conditions": {"all": [
        {"name": "cantidad_comentarios",
         "operator": "greater_than",
         "value": 2
         }
    ]},
     "actions": [
         {"name": "incrementar_importancia",
          "params": {"cantidad": 2}}
     ]
    },
    # reacciones > 2: +1
    {"conditions": {"all": [
        {"name": "cantidad_me_gusta",
         "operator": "greater_than",
         "value": 2
         }
    ]},
     "actions": [
         {"name": "incrementar_importancia",
          "params": {"cantidad": 1}}
     ]
    },
    # ya reaccione: -5
    {"conditions": {"all": [
        {"name": "mi_reaccion",
         "operator": "non_empty",
         "value": ""
         }
    ]},
     "actions": [
         {"name": "decrementar_importancia",
          "params": {"cantidad": 5}}
     ]
    },
    # más viejo que 2hs: -1
    {"conditions": {"all": [
        {"name": "antiguedad",
         "operator": "greater_than",
         "value": 2 * 3600
         }
    ]},
     "actions": [
         {"name": "decrementar_importancia",
          "params": {"cantidad": 1}}
     ]
    },
    # contactos > 2: +1
    {"conditions": {"all": [
        {"name": "cantidad_contactos",
         "operator": "greater_than",
         "value": 2
         }
    ]},
     "actions": [
         {"name": "incrementar_importancia",
          "params": {"cantidad": 1}}
     ]
    }
]
