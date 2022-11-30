import os
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route("/env")
class HelloEnvironment(Resource):
    def get(self):
        return dict(os.environ)
    
