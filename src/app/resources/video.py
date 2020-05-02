from flask_restful import Resource
from flask import request

class Video(Resource):
    def post(self):
        body = request.get_json(force=True)
        url = body['url']
        titulo = body['titulo']

        return {'titulo': titulo, 'url': url}
