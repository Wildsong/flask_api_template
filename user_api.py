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
        users = db.session.execute(db.select(User).order_by(User.username)).all()
        l = [u[0].__dict__ for u in users] # return rows as a list of dicts 
        return l
    def getUser(self, id: int) -> object:
        try:
            # https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.select
            u = db.session.execute(db.select(User).where(User.id==id)).one()[0]
        except Exception as e:
            api.abort(404, f'User {id} not found.')
        return u
    def get(self, id: int) -> dict:
        u = self.getUser(id)
        return u.__dict__ # return row as a dict
    def create(self, data: object) -> object:
        u = User()
        try:
            u = User()
            u.username = data['username']
            if 'password' in data: u.password = data['password']
            if 'role' in data: u.role = data['role']
            db.session.add(u)
            db.session.commit()
        except Exception as e:
            print(e)
            api.abort(404, f"User '{data['username']}' create failed.")
        return u
    def update(self, id: int, data: dict) -> dict:
        u = self.getUser(id)
        try:
            if 'username' in data: u.username = data['username']
            if 'password' in data: u.password = data['password']
            if 'role'     in data: u.role     = data['role']
        except Exception as e:
            print(e)
            api.abort(404, f'User {id} could not be updated.')
        db.session.commit()
        return u
    def delete(self, id: int) -> None:
        u = self.getUser(id)
        try:
            db.session.delete(u)
            db.session.commit()
            s = 'deleted'
        except Exception as e:
            print(e)
            api.abort(404, f'User {id} delete failed.')
        return u.__dict__

dao = UserDAO()

# This defines what the API sees when it marshals a user from the database
userModel = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'role': fields.String
})

def UserAlreadyExists(Error):
    return
@ns.route('/') # This will be the URL with a slash at the end, http://127.0.0.1:5000/user/
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(userModel)
    def get(self):
        """ Return a JSON formatted list of all users in the database. """
        # I want to return the URL for each user
        return dao.getAll()

    @ns.doc('create_todo')
    @ns.expect(userModel)
    @ns.marshal_with(userModel, code=201)
    def post(self):
        """ Add a new user to the database. """
        # I want to return the URL for the updated user
        return dao.create(api.payload), 201
        

@ns.route('/<int:id>')
@ns.response(404, 'User not found')
class UserApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
        help='Login name of a user', location='json')

    @ns.doc('get_user')
    @ns.marshal_with(userModel)
    def get(self, id):
        """ Return information on a user matching the requested id. """
        # I want to return the URL for the updated user
        return dao.get(id)

    @ns.doc('update_user')
    @ns.expect(userModel)
    @ns.marshal_with(userModel, code=201)
    def put(self, id):
        """ Update an existing user. """
        # I want to return the URL for the updated user
        return dao.update(id, api.payload), 201
        
    @ns.doc('delete_user')
    def delete(self, id):
        return dao.delete(id)

