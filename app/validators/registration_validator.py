import re
from flask import jsonify
from models.user import User

user_collection = User()

allowed_role = ["admin", "user_management"]


def is_validate_username(username: str):
    if len(username) >= 6:
        return True, ""
    return False, "Username has to at least 6 characters"


def is_validate_password(password: str):
    if len(password) >= 8:
        return True, ""
    return False, "Password has to at least 8 characters"


def is_validate_email(email: str):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    result = re.match(email_regex, email)
    if result is not None:
        return True, ""
    return False, "Invalid email format"


def is_existed_mail(email: str):
    try:
        query = {
            "email": email
        }
        user = user_collection.get_user_by_query(query)
        if user:
            return False, "Email is existed!"
        return True, ""
    except Exception as e:
        return jsonify({
            "message": f"Error is occured {e}", "status": 500}), 500


def is_existed_username(username: str):
    try:
        query = {
            "username": username
        }
        user = user_collection.get_user_by_query(query)
        if user:
            return False, "Username is existed!"
        return True, ""
    except Exception as e:
        return jsonify({
            "message": f"Error is occured {e}", "status": 500}), 500


def check_allowed_role(role: str):
    if role not in allowed_role:
        return False, "You dont have right to create this role!"
    return True, ""


def validate_registation_data(user_data: dict):
    data = user_data.keys()
    if "username" not in data or "password" not in data or "email" not in data:
        return jsonify({"message": "Missing required fields", "status": 400}),

    username: str = user_data["username"]
    password: str = user_data["password"]
    email: str = user_data["email"]

    is_valid_username, message = is_validate_username(username)
    if not is_valid_username:
        return jsonify({
            "message": message,
            "status": 400
        })

    is_valid_password, message = is_validate_password(password)
    if not is_valid_password:
        return jsonify({
            "message": message,
            "status": 400
        })

    is_valid_email, message = is_validate_email(email)
    if not is_valid_email:
        return jsonify({
            "message": message,
            "status": 400
        })

    is_existed_username, message = is_existed_mail(username)
    if not is_existed_username:
        return jsonify({
            "message": message,
            "status": 400
        })

    is_existed_email, message = is_existed_mail(email)
    if not is_existed_email:
        return jsonify({
            "message": message,
            "status": 400
        })

    user_role: str = user_data["role"]

    is_can_create_role, message = check_allowed_role(user_role)
    if not is_can_create_role:
        return jsonify({
            "message": message,
            "status": 403
        }), 403
    return None
