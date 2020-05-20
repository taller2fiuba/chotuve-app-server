from flask_restful import Resource

class Ping(Resource):
   def get(self):
        return {}, 200, {'Access-Control-Allow-Origin': '*'}
