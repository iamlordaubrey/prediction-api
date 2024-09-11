import jwt

from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

from config.app_config import Config
from models.user import User


def create_jwt_token(user_id):
    """
    Create a JWT token for the user.
    """
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        'user_id': user_id,
        'exp': expiration
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def decode_jwt_token(token):
    """
    Decode the JWT token and return the payload.
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to ensure the request has a valid JWT token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found!'}), 404

        return f(user, *args, **kwargs)

    return decorated
