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


def test_get_course_by_id_not_found(client):
    response = client.get('/courses/605c72f1a6d4c194708aeb41')
    assert response.status_code == 404
    assert 'Course is not found' in response.json['message']


def test_update_course_invalid_data(client):
    data = {
        "duration": "five"
    }
    response = client.put('/courses/605c72f1a6d4c194708aeb41', json=data)
    assert response.status_code == 500
    assert 'Failed to get information of course' in response.json['message']


def test_delete_course_not_found(client, mocker):
    mocker.patch('models.course.Course.delete_course',
                 return_value=mocker.Mock(deleted_count=0))

    response = client.delete('/courses/605c72f1a6d4c194708aeb41')
    assert response.status_code == 404
    assert 'Can not delete course' in response.json['message']
