from flask import Blueprint
from controllers.course_controller import (
    create_course,
    get_all_course,
    get_course_by_id,
    update_course_by_id,
    detele_course_by_id
)
course_bp = Blueprint("course_bp", __name__)


@course_bp.route('/courses', methods=["POST"])
def create_course_route():
    return create_course()


@course_bp.route('/courses', methods=["GET"])
# @token_required()
def get_all_course_route():
    return get_all_course()


@course_bp.route('/courses/<course_id>', methods=["GET"])
def get_course_by_id_route(course_id):
    return get_course_by_id(course_id)


@course_bp.route('/courses/<course_id>', methods=["PUT"])
def update_course_by_id_route(course_id):
    return update_course_by_id(course_id)


@course_bp.route('/courses/<course_id>', methods=["DELETE"])
def detele_course_by_id_route(course_id):
    return detele_course_by_id(course_id)
