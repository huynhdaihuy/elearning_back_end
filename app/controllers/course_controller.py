from flask import jsonify, request
from models.course import Course

course_collection = Course()


def create_course():
    required_fields = ['name', 'description',
                       'duration', 'rating', 'instructor', 'enrolled_student']
    data: dict = request.get_json()
    data_fields = data.keys()
    for field in required_fields:
        if field not in data_fields:
            return jsonify({
                "status": 401,
                "message": f"Missing required field: {field}",
                "data": None}), 401

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
            }}), 201
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to create course: {str(e)}"}), 500


def get_all_course():
    try:
        courses = course_collection.get_all_course()
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": courses
        }), 200
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course {e}"})


def get_course_by_id(course_id):
    try:
        course = course_collection.get_course_by_id(course_id)
        if not course:
            return jsonify({
                "status": 404,
                "message": "Course is not found!",
                "data": course
            }), 404
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": course
        }), 200
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course {e}"}), 500


def update_course_by_id(course_id):
    data = request.get_json()
    try:
        result = course_collection.update_course(
            course_id, data)
        is_updated = (result.raw_result)['updatedExisting']
        print(f'RESULT {is_updated}')
        if not is_updated:
            return jsonify({
                "data": None,
                "status": 500,
                "message": f"Failed to get information of course with id: {course_id}"}), 500
        if result.modified_count:
            return jsonify({
                "data": {
                    "_id": course_id
                },
                "status": 200,
                "message": "Course is updated successfully"}), 200

        return jsonify({
            "status": 200,
            "message": "There is no change in database",
            "data": None}), 200
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course: {str(e)}"}), 500


def detele_course_by_id(course_id):
    try:
        deleted_data = course_collection.delete_course(course_id)
        if deleted_data.deleted_count:
            return jsonify({
                "status": 200,
                "message": "Course is deleted successfully",
                "data": None
            }, 204), 204
        else:
            return jsonify({
                "status": 404,
                "message": "Can not delete course",
                "data": None}), 404
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": f"Failed to get information of course: {str(e)}"}), 500
