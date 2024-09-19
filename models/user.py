from util import (serialize, serialize_except_pw, db)
from bson.objectid import ObjectId


class User:
    def __init__(self) -> None:
        self.collection = db["user"]

    def get_all_user(self):
        users = self.collection.find({})
        return [serialize(user) for user in users]

    def get_user_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return serialize(user)

    def get_user_by_query(self, query):
        user = self.collection.find_one(query)
        return serialize_except_pw(user)

    def create_user(self, user_data):
        return self.collection.insert_one(user_data)

    def update_user(self, user_id, update_field):
        return self.collection.update_one({
            "_id": ObjectId(user_id),
        }, {"$set": update_field})

    def update_otp_check_count(self, user_id, updated_count):
        return self.collection.update_one({
            "_id": ObjectId(user_id),
        }, {"$set": {"otp_infor.otp_check_count": updated_count}})

    def verify_mail(self, user_id):
        return self.collection.update_one({
            "_id": ObjectId(user_id),
        }, {"$set": {"is_verified": True}})

    def block_user(self, user_id):
        return self.collection.update_one({
            "_id": ObjectId(user_id),
        }, {"$set": {"is_disabled": True}})

    def delete_user(self, user_id):
        return self.collection.delete_one({"_id": ObjectId(user_id)})

    def delete_users(self):
        return self.collection.delete_many({})

    def upload_avatar(self, user_id, image_url):
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"url_avatar": image_url}}
        )

    def generate_otp_infor(self, user_id, otp_infor):
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"otp_infor": otp_infor}}
        )
