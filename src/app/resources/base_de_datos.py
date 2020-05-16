from flask_restful import Resource

import auth_server_api
from app import app, db

class BaseDeDatosResource(Resource):
    if app.config.get('FLASK_ENV') == 'development':
        def delete(self):
            response = auth_server_api.limpiar_base_de_datos()
            if response.status_code == 200:
                meta = db.metadata
                for tabla in reversed(meta.sorted_tables):
                    # TODO logger
                    print(f'Limpiando tabla {tabla}')
                    db.session.execute(tabla.delete())
                db.session.commit()
                return {}, 200
            return {}, response.status_code
