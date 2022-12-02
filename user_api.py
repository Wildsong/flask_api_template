import os
from flask import Flask, Response, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api, reqparse, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="User API", description="User management API")

ns = api.namespace('user', description='User database stuff')

# -- Database model --
db = SQLAlchemy(app)

# Define a class for each table.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)

# This will create the database and tables if they don't exist
with app.app_context():
    db.create_all()

# This data access object encapsulates all access to our datastore.
class UserDAO(object):

    def __init__(self) -> None:
        return
    def getAll(self) -> list:
        users = db.session.execute(db.select(User)).all()
        l = [{"id":user[0].id, "username":user[0].username} for user in users]
    def get(self, id: int) -> object:
        user = db.session.execute(db.select(User, id=id)).one()
        return {"id":user[0].id, "username":user[0].username}
    def create(self, username) -> object:
        user = None
        try:
            user = User(
                username=username,
                password="joe",
                role="Producer"
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise UserAlreadyExists
    def update(self, id: int, data: object) -> object:
        return
    def delete(self, id: int) -> None:
        return

dao = UserDAO()

# This defines what the API sees when it marshals a user from the database
userModel = api.model('User', {
    'username': fields.String
})

def UserAlreadyExists(Error):
    return
@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')

    @ns.marshal_list_with(userModel)
    def get(self):
        """ Return a JSON formatted list of all users in the database. """


@ns.route('/user/<int:id>', methods=["GET"])
@api.route('/user', methods=["POST"])
class UserApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
        help='Login name of a user', location='json')

    def get(self, id):
        """ Return information on a user matching the requested id. """
        user = db.session.execute(db.select(User).filter_by(id=id)).one()
        u = {"id":user[0].id, "username":user[0].username}
        return u

    def post(self):
        """ Add a new user to the database. """
        args = self.parser.parse_args()
        u = args['username'].lower()
        return dao.create(u)
        
    def delete(self):
        print("DELETE!")
        return jsonify(count=1)

