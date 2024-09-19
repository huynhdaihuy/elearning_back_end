from functools import wraps
from flask import jsonify, request
from controllers.auth_controller import (verify_access_token)
from models.user import User

user_collection = User()


def token_required(expected_role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({
                    "message": "Missing Authorization header",
                    "status": 401
                }), 401
            try:
                token = auth_header.split(" ")[1]
                user_id = verify_access_token(token)
                if not user_id:
                    return jsonify({
                        "message": "Invalid or expired token",
                        "status": 401
                    }), 401
                user = user_collection.get_user_by_id(user_id)
                if expected_role and user["role"] != expected_role:
                    return jsonify({
                        "status": 403,
                        "data": None,
                        "message": "Forbidden: You do not have the required right to access this resource"}), 403
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    "status": 500,
                    "data": None,
                    "message": "Unexpected error is occured {e}"}), 500
        return decorated_function
    return decorator
