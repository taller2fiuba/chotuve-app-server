from flask_restful import Resource

from app import app, db, log
from app.servicios import auth_server, media_server

class BaseDeDatosResource(Resource):
    if app.config.get('FLASK_ENV') == 'development':
        def delete(self):
            if not auth_server.limpiar_base_de_datos():
                return {'mensaje': 'No se pudo limpiar la base del auth.'}, 500
            if not media_server.limpiar_base_de_datos():
                return {'mensaje': 'No se pudo limpiar la base del media.'}, 500

            meta = db.metadata
            for tabla in reversed(meta.sorted_tables):
                log.info('Limpiando tabla %r', str(tabla))
                db.session.execute(tabla.delete())
            db.session.commit()
            return {}, 200
