from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
l = list()

parser = reqparse.RequestParser()
parser.add_argument('item', type=str, help='Something to add to the list.')

@api.route('/list')
class List(Resource):
    def get(self):
        return l

    def post(self):
        args = parser.parse_args()
        l.append(args['item'])
        return jsonify(count = len(l))

    def delete(self):
        global l
        args = parser.parse_args()
        l = [x for x in l if x != args['item']]
        return jsonify(count = len(l))

