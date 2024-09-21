from flask import Blueprint
from controllers.user_controller import (
    get_all_user,
    get_user_by_id,
    detele_user_by_id,
    detele_users,
    upload_avatar,
    update_infor_user
)
from middlewares.token_middleware import token_required
user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/user', methods=["GET"])
@token_required(expected_role="user")
def get_all_user_route():
    return get_all_user()


@user_bp.route('/user/<user_id>', methods=["GET"])
def get_user_by_id_route(user_id):
    return get_user_by_id(user_id)


@user_bp.route('/user/<user_id>', methods=["DELETE"])
def detele_user_by_id_route(user_id):
    return detele_user_by_id(user_id)


@user_bp.route('/user/<user_id>', methods=["PUT"])
def update_user_by_id_route(user_id):
    return update_infor_user(user_id)


@user_bp.route('/user/', methods=["DELETE"])
def detele_users_route():
    return detele_users()


@user_bp.route('/user/upload-avatar/<user_id>', methods=["POST"])
def upload_user_route(user_id):
    return upload_avatar(user_id)
