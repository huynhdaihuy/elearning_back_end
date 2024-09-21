from util import (serialize_except_pw, db)
from bson.objectid import ObjectId


class Course:
    def __init__(self) -> None:
        self.collection = db["course"]

    def create_course(self, course_data):
        return self.collection.insert_one(course_data)

    def get_all_course(self):
        courses = self.collection.find()
        return [serialize_except_pw(course) for course in courses]

    def get_course_by_id(self, course_id):
        course = self.collection.find_one({"_id": ObjectId(course_id)})
        return serialize_except_pw(course)

    def update_course(self, course_id, course_data):
        return self.collection.update_one({
            "_id": ObjectId(course_id),
        }, {"$set": course_data})

    def delete_course(self, course_id):
        return self.collection.delete_one({"_id": ObjectId(course_id)})
