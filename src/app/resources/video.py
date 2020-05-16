from flask_restful import Resource
from flask import request
import requests
from app import app

CHOTUVE_MEDIA_URL = app.config.get('CHOTUVE_MEDIA_URL')

class Video(Resource):
    def post(self):
        body = request.get_json(force=True)
        url = body['url']
        titulo = body['titulo']

        response = requests.post(
            CHOTUVE_MEDIA_URL + "/video", json={"url": url, "titulo": titulo})

        return response.json(), response.status_code
