REGLAS = [
    # comentarios < 20, reacciones < 5
    {"conditions": {"all": [
        {"name": "cantidad_reacciones",
         "operator": "less_than",
         "value": 5
         },
        {"name": "cantidad_comentarios",
         "operator": "less_than",
         "value": 20
         }
    ]},
     "actions": [
         {"name": "decrementar_importancia",
          "params": {"cantidad": 1}
          }]
    },
    # comentarios > 20, reacciones > 20
    {"conditions": {"all": [
        {"name": "cantidad_reacciones",
         "operator": "greater_than",
         "value": 20
         },
        {"name": "cantidad_comentarios",
         "operator": "greater_than",
         "value": 20
         }
    ]},
     "actions": [
         {"name": "incrementar_importancia",
          "params": {"cantidad": 1}
          }]
    }
]
