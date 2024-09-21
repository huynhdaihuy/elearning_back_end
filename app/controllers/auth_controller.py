import datetime
import random
import jwt
import bcrypt
from flask import (jsonify, request, current_app)
from config.config import (
    SECRET_KEY, REFRESH_SECRET_KEY, EMAIL_VERIFICATION_SECRET_KEY)
from validators.registration_validator import validate_registation_data
from models.user import User
from service.mail_service import MailService

ALGORITHM = "HS256"
user_collection = User()


def register():
    user_data = request.get_json()
    validatior_error = validate_registation_data(user_data)
    if validatior_error:
        return validatior_error
    password: str = user_data["password"]
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user_added = user_collection.create_user({
            "email": user_data["email"],
            "username": user_data["username"],
            "password": hashed_password,
            "is_verified": False,
            "is_disabled": False,
            "role": user_data["role"]
        })
        mail_service: MailService = current_app.extensions["mail_service"]
        user_id = user_added.inserted_id
        verify_mail_token = generate_verify_email_token(str(user_id))
        mail_service.send_verify_mail(
            "huynhdaihuybank6@gmail.com", verify_mail_token)
        return jsonify({
            "status": 201,
            "message": "User is registered successfully",
            "data": {
                "user_id": str(user_added.inserted_id)}})
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to register user: {str(e)}"})


def login():
    user_data = request.get_json()
    username: str = user_data["username"]
    password: str = user_data["password"]
    try:
        user = user_collection.get_user_by_query({'username': username})
        if user and bcrypt.checkpw(password.encode(), user['password']):
            access_token = generate_access_token(str(user["_id"]))
            refresh_token = generate_refresh_token(str(user["_id"]))
            return jsonify({
                "status": 201,
                "message": "Login successfully",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token}})
        return jsonify({
            "status": 404,
            "message": "Your account is inactive or wrong password",
            "data": None})

    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to login user: {str(e)}"})


def generate_access_token(user_id: str):
    expiration = datetime.datetime.now(
        datetime.UTC) + datetime.timedelta(hours=24)
    token = jwt.encode({
        "user_id": user_id,
        "exp": expiration
    }, SECRET_KEY, ALGORITHM)
    print(f"ACCESSTOKEN {token}")
    return token


def generate_refresh_token(user_id: str):
    expiration = datetime.datetime.now(
        datetime.UTC) + datetime.timedelta(days=7)
    rf_token = jwt.encode({
        "user_id": user_id,
        "exp": expiration
    }, REFRESH_SECRET_KEY, ALGORITHM)
    return rf_token


def generate_verify_email_token(user_id: str):
    expiration = datetime.datetime.now(
        datetime.UTC) + datetime.timedelta(days=7)
    verify_token = jwt.encode({
        "user_id": user_id,
        "exp": expiration
    }, EMAIL_VERIFICATION_SECRET_KEY, ALGORITHM)
    return verify_token


def verify_access_token(token):
    if not token:
        return jsonify({
            "status": 400,
            "data": None,
            "message": "Token is missing"
        }), 400
    try:
        decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = decoded["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def verify_refresh_token(rf_token):
    if not rf_token:
        return jsonify({
            "status": 400,
            "data": None,
            "message": "Token is missing"
        }), 400
    try:
        decoded = jwt.decode(rf_token, REFRESH_SECRET_KEY, ALGORITHM)
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def verify_email_token(email_token):
    if not email_token:
        return jsonify({
            "status": 400,
            "data": None,
            "message": "Token is missing"
        }), 400
    try:
        decode = jwt.decode(
            email_token, EMAIL_VERIFICATION_SECRET_KEY, ALGORITHM)
        user_id = decode["user_id"]
        user = user_collection.get_user_by_id(user_id)
        if not user:
            return jsonify({
                "status": 404,
                "data": None,
                "message": "User not found"
            }), 404
        user_collection.verify_mail(user_id)
        return jsonify({
            "status": 200,
            "data": None,
            "message": "User has verified email successfully!"
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": 400,
            "data": None,
            "message": "Verification token has expired!"
        }), 400
    except jwt.InvalidKeyError:
        return jsonify({
            "status": 400,
            "data": None,
            "message": "Verification token is invalid!"
        }), 400


def generate_otp_code(username):
    user = user_collection.get_user_by_query({
        "username": username
    })
    if user is None:
        return jsonify({
            "status": 404,
            "message": "username is wrong or invalid",
            "data": None}), 404
    otp = random.randint(100000, 999999)
    expiration = datetime.datetime.now(
        datetime.UTC) + datetime.timedelta(minutes=5)
    expiration_timestamp = expiration.timestamp()
    otp_info = {
        "code": otp,
        "exp": expiration_timestamp,
        "otp_check_count": 3
    }
    user_id = user["_id"]
    user_collection.generate_otp_infor(user_id, otp_info)
    mail_service: MailService = current_app.extensions["mail_service"]
    mail_service.send_otp_mail("huynhdaihuybank3@gmail.com", otp)
    return jsonify({
        "status": 201,
        "message": "Generate otp successfully",
        "data": otp_info}), 201


def verify_otp_infor():
    infor = request.get_json()
    otp_code = infor["otp_code"]
    username = infor["username"]
    query = {
        "username": username
    }
    user = user_collection.get_user_by_query(query)
    if user is None:
        return jsonify({
            "status": 404,
            "message": "username is wrong or invalid",
            "data": None}), 404
    otp_infor = user["otp_infor"]
    checking_count = otp_infor["otp_check_count"]
    if checking_count == 0:
        user_collection.block_user(user["_id"])
        return jsonify({
            "status": 404,
            "message": "You are blocked, you have entered wrong many times",
            "data": None}), 404
    checking_count -= 1
    expiration = otp_infor["exp"]
    is_invalid_otp = datetime.datetime.now(
        datetime.timezone.utc).timestamp() > expiration
    if is_invalid_otp:
        return jsonify({
                       "status": 400,
                       "message": "OTP code is expired, get otp code and try again!",
                       "data": None}), 400

    match_otp = otp_code == otp_infor["code"]
    if not match_otp:
        user_collection.update_otp_check_count(user["_id"], checking_count)
        return jsonify({
            "status": 400,
            "message": f"OTP code is wrong, get otp code and try again. You have {checking_count + 1} times to try!",
            "data": None}), 400

    access_token = generate_access_token(user["_id"])
    refresh_token = generate_refresh_token(user["_id"])
    return jsonify({
        "status": 200,
        "message": "Login is successfully!",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }}), 200
