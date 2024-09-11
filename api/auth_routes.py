from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields

from config.db_config import db
from models.user import User
from services.jwt_handler import create_jwt_token
from utils.api_logger import log_api_call
from utils.error_handler import handle_error

auth_namespace = Namespace('auth', description='Authentication related operations')

register_model = auth_namespace.model('Register', {
    'username': fields.String(required=True, description='Username for the new user'),
    'password': fields.String(required=True, description='Password for the new user')
})

login_model = auth_namespace.model('Login', {
    'username': fields.String(required=True, description='Username for login'),
    'password': fields.String(required=True, description='Password for login')
})


@auth_namespace.route('/register')
class RegisterUser(Resource):
    @auth_namespace.expect(register_model, validate=True)
    @auth_namespace.response(201, 'User registered successfully')
    @auth_namespace.response(400, 'Username and password are required or username already exists')
    @auth_namespace.response(500, 'Internal Server Error')
    def post(self):
        """
        Register a new user
        """
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return handle_error('Username and password are required', 400)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return handle_error('Username already exists', 400)

        new_user = User(username=username)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return handle_error('Error registering user: ' + str(e), 500)

        log_api_call(username, 'register', request.json)
        return make_response(jsonify({'message': 'User registered successfully'}), 201)


@auth_namespace.route('/login')
class LoginUser(Resource):
    @auth_namespace.expect(login_model, validate=True)
    @auth_namespace.response(200, 'Login successful, JWT token returned')
    @auth_namespace.response(400, 'Username and password are required')
    @auth_namespace.response(401, 'Invalid username or password')
    @auth_namespace.response(500, 'Internal Server Error')
    def post(self):
        """
        Login a user and return a JWT token.
        """
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return handle_error('Username and password are required', 400)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = create_jwt_token(user.id)
            log_api_call(username, 'login', request.json)
            return make_response(jsonify({'token': token}), 200)

        return handle_error('Invalid username or password', 401)
