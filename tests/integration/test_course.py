
def test_create_course(client):
    mock_data = {
        "name": "Name mock data test_create_course",
        "description": "Description mock Test.",
        "duration": 10,
        "rating": 0,
        "instructor": "Intructor mock data",
        "enrolled_student": 0
    }
    respone = client.post('courses', json=mock_data)

    assert respone.status_code == 201
    assert respone.get_json()['message'] == 'Course is created successfully'


def test_get_courses(client, mongo):
    mock_data = {
        "name": "Test get courses name test_get_courses",
        "description": "Test get courses description"
    }
    course_id = str(mongo.course.insert_one(mock_data).inserted_id)
    respone = client.get('/courses')
    courses = respone.get_json()['data']
    assert len(courses) > 0
    assert respone.status_code == 200
    assert any(course["_id"] ==
               course_id for course in courses)


def test_get_course_by_id(client, mongo):
    mock_data = {
        "name": "Test get courses name test_get_course_by_id",
        "description": "Test get courses description test_get_course_by_id"
    }
    course_id = str(mongo.course.insert_one(
        mock_data).inserted_id)
    respone = client.get(f'/courses/{course_id}')
    course = respone.get_json()['data']
    assert respone.status_code == 200
    assert course_id == course['_id']


def test_update_course(client, mongo):
    mock_data = {
        "name": "Test get courses name test_update_course",
        "description": "Test get courses description test_update_course"
    }
    course_id = str(mongo.course.insert_one(mock_data).inserted_id)
    update_data = {
        'name': 'Test update course test_update_course'}

    respone = client.put(f'courses/{str(course_id)}', json=update_data)
    data = respone.get_json()['data']
    updated_course_id = data['_id']

    assert respone.status_code == 200
    assert updated_course_id == course_id


def test_delete_course(client, mongo):
    mock_data = {
        "name": "Test get courses name test_delete_course",
        "description": "Test get courses description test_delete_course"
    }
    course_id = str(mongo.course.insert_one(mock_data).inserted_id)
    respone = client.delete(f'/courses/{course_id}')
    assert respone.status_code == 204
