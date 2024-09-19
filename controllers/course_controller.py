
from flask import jsonify, request
from models.course import Course


course_collection = Course()


def create_course():
    data = request.get_json()
    course = {
        "name": data["name"],
        "description": data["description"],
        "duration": data["duration"],
        "rating": data["rating"],
        "instructor": data["instructor"],
        "enrolled_student": data["enrolled_student"]
    }
    try:
        insert_result = course_collection.create_course(course)
        return jsonify({
            "status": 201,
            "message": "Course is created successfully",
            "data": {
                "course_id": str(insert_result.inserted_id)
            }})
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to create course: {str(e)}"})


def get_all_course():
    try:
        courses = course_collection.get_all_course()
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": courses
        })
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course {e}"})


def get_course_by_id(course_id):
    try:
        course = course_collection.get_course_by_id(course_id)
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": course
        })
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course {e}"})


def update_course_by_id(course_id):
    data = request.get_json()
    update_data = {
        "name": data["name"],
        "description": data["description"],
        "duration": data["duration"]
    }
    try:
        updated_data = course_collection.update_course(course_id, update_data)
        if updated_data.matched_count:
            return jsonify({
                "data": update_data,
                "status": 200,
                "message": "Course is updated successfully"})
        else:
            return jsonify({
                "status": 404,
                "message": "Can not save course",
                "data": None})
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course: {str(e)}"})


def detele_course_by_id(course_id):
    try:
        deleted_data = course_collection.delete_course(course_id)
        if deleted_data.deleted_count:
            return jsonify({
                "status": 200,
                "message": "Course is deleted successfully",
                "data": None
            }, 200)
        else:
            return jsonify({
                "status": 404,
                "message": "Can not delete course",
                "data": None})
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course: {str(e)}"})
