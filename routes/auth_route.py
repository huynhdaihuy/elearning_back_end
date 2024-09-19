from flask import Blueprint
from controllers.auth_controller import (
   register,
   login,
   generate_access_token,
   generate_refresh_token,
   generate_otp_code,
   verify_otp_infor,
   verify_email_token
)

auth_bp = Blueprint("auth_bp",__name__)

@auth_bp.route('/auth/register',methods=["POST"])
def register_route():
    return register()

@auth_bp.route('/auth/login',methods=["POST"])
def login_route():
    return login()

@auth_bp.route('/auth/access-token/<user_id>',methods=["GET"])
def get_access_token_route(user_id):
    return generate_access_token(user_id)
    
@auth_bp.route('/auth/refresh-token/<user_id>',methods=["GET"])
def get_refresh_token_route(user_id):
    return generate_refresh_token(user_id)

@auth_bp.route('/auth/generate-otp/<username>',methods=["GET"])
def generate_otp_code_route(username):
    return generate_otp_code(username)

@auth_bp.route('/auth/verify-otp/',methods=["POST"])
def verify_otp_code_route():
    return verify_otp_infor()

@auth_bp.route('/auth/verify-email/<token>',methods=["GET"])
def verify_mail_route(token):
    return verify_email_token(token)