
from flask import jsonify, request
from models.user import User
from service.upload_service import UploadService
from util import serialize
user_collection = User()
upload_service = UploadService()


def get_all_user():
    try:
        users = user_collection.get_all_user()
        print("ISGETTINGALLUSER")
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": users
        }), 200
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of user {e}"}), 500


def get_user_by_id(user_id):
    try:
        user = user_collection.get_user_by_id(user_id)
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": serialize(user)
        }), 200
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of user {e}"}), 500


def detele_user_by_id(user_id):
    try:
        deleted_data = user_collection.delete_user(user_id)
        if deleted_data.deleted_count:
            return jsonify({
                "status": 200,
                "message": "User is deleted successfully",
                "data": None
            }), 200
        else:
            return jsonify({
                "status": 404,
                "message": "Can not delete user",
                "data": None})
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to delete information of course: {str(e)}"}), 500


def detele_users():
    try:
        deleted_data = user_collection.delete_users()
        if deleted_data.deleted_count:
            return jsonify({
                "status": 200,
                "message": "All users are deleted successfully",
                "data": None
            }), 200
        else:
            return jsonify({
                "status": 404,
                "message": "Can not delete users",
                "data": None}), 404
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to delete information of users: {str(e)}"}), 500


def upload_avatar(user_id):
    if 'avatar' not in request.files:
        return jsonify({
            "status": 400,
            "message": "No file provided"}), 400
    if not user_id:
        return jsonify({
            "status": 400,
            "message": "No user_id provided"}), 400

    file = request.files['avatar']
    image_url = upload_service.upload_file(file, folder="avatars/")

    if image_url:
        try:
            user_updated = user_collection.upload_avatar(user_id, image_url)
            return jsonify({
                "message": "Upload avatar is successfully!",
                "status": 200,
                "data": {
                    "image_url": image_url}}), 200
        except Exception as e:
            return jsonify({
                "message": "An error is happen while uploading! {e}",
                "status": 400,
                "data": None}), 400
    else:
        return jsonify({
            "status": 500,
            "message": "Failed to upload avatar"}), 500


def update_infor_user(user_id):
    update_field = request.get_json()
    if not user_id:
        return jsonify({
            "message": "user_id is wrong or invalid",
            "status": 404,
            "data": None}), 404
    try:
        result = user_collection.update_user(user_id, update_field)
        if result.matched_count == 0:
            return jsonify({
                "message": "User not found",
                "status": 404
            }), 404

        if result.modified_count == 0:
            return jsonify({
                "message": "No changes made to the user information",
                "status": 200
            }), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to update user {e}"}), 500
