import pytest


@pytest.mark.skip(reason='Misunderstood the API')
def test_create_course_missing_field(client):
    mock_data = {
        "description": "Python programming course",
        "duration": 5,
        "rating": 4.5,
        "instructor": "John Doe",
        "enrolled_student": 200
    }
    response = client.post('/courses', json=mock_data)
    assert response.status_code == 401
    assert 'Missing required field' in response.json['message']


@pytest.mark.exception
@pytest.mark.exception_type
def test_create_course_wrong_type(client):
    mock_data = {
        "name": "Course Python Test",
        "description": "Python programming course",
        "duration": '5',
        "rating": 4.5,
        "instructor": "John Doe",
        "enrolled_student": 200
    }
    with pytest.raises(TypeError) as expinfo:
        response = client.post('/courses', json=mock_data)
    exp_msg = expinfo.value.args[0]
    assert exp_msg == 'duration must be an integer'


@pytest.mark.exception
@pytest.mark.exception_value
def test_create_course_wrong_value(client):
    mock_data = {
        "name": "Course Python Test",
        "description": "Python programming course",
        "duration": -5,
        "rating": 4,
        "instructor": "John Doe",
        "enrolled_student": 200
    }
    with pytest.raises(ValueError) as expinfo:
        response = client.post('/courses', json=mock_data)
    exp_msg = expinfo.value.args[0]
    assert exp_msg == 'duration must be greater than 0'


def test_get_course_by_id_not_found(client):
    response = client.get('/courses/605c72f1a6d4c194708aeb41')
    assert response.status_code == 404
    assert 'Course is not found' in response.json['message']


def test_update_course_invalid_data(client, mongo):
    mock_data = {
        "name": "Course Python Test Update Invalid",
        "description": "Python programming course",
        "duration": 10,
        "rating": 0,
        "instructor": "John Doe",
        "enrolled_student": 200
    }
    course_id = str(mongo.course.insert_one(mock_data).inserted_id)
    update_data = {
        "duration": 0,
    }

    response = client.put(f'courses/{str(course_id)}', json=update_data)
    data = response.get_json()['data']
    updated_course_id = data['_id']

    assert response.status_code == 200
    assert updated_course_id == course_id


def test_delete_course_not_found(client):
    response = client.delete('/courses/605c72f1a6d4c194708aeb41')
    assert response.status_code == 404
    assert 'Can not delete course' in response.json['message']
