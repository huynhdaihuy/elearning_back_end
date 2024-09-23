def test_get_users(client, mongo):
    mock_data_user = {"name": "user's test_get_users",
                      "email": "test_get_users@gmail.com",
                      "username": "test_get_users_username",
                      "password": "123456789",
                      "role": "user",
                      }
    user_id = str(mongo.user.insert_one(mock_data_user).inserted_id)
    response = client.get('/user')
    users = response.get_json()['data']
    assert len(users) > 0
    assert response.status_code == 200
    assert any(user["_id"] ==
               user_id for user in users)


def test_get_user_by_id(client, mongo):
    mock_data_user = {"name": "user's test_get_user_by_id",
                      "email": "test_get_user_by_id@gmail.com",
                      "username": "test_get_user_by_id_username",
                      "password": "123456789",
                      "role": "user",
                      }
    user_id = str(mongo.user.insert_one(
        mock_data_user).inserted_id)
    response = client.get(f'/user/{user_id}')
    user = response.get_json()['data']
    assert response.status_code == 200
    assert user_id == user['_id']


def test_update_user(client, mongo):
    mock_data_user = {"name": "user's test_update_user",
                      "email": "test_update_user@gmail.com",
                      "username": "test_update_user_username",
                      "password": "123456789",
                      "role": "user",
                      }
    user_id = str(mongo.user.insert_one(mock_data_user).inserted_id)
    update_data = {
        'name': 'user"s name updated'}
    response = client.put(f'user/{str(user_id)}', json=update_data)
    msg = response.get_json()['message']
    assert response.status_code == 200
    assert 'User is updated successfully' in msg


def test_delete_user_by_id(client, mongo):
    mock_data_user = {"name": "user's test_delete_user_by_id",
                      "email": "test_delete_user_by_id@gmail.com",
                      "username": "test_delete_user_by_id_username",
                      "password": "123456789",
                      "role": "user",
                      }
    user_id = str(mongo.user.insert_one(mock_data_user).inserted_id)
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 204


def test_delete_all_user(client, mongo):
    mock_data_user1 = {"name": "user's name test_delete_all_user",
                       "email": "test_delete_all_user@gmail.com",
                       "username": "test_delete_all_user_username",
                       "password": "123456789",
                       "role": "user",
                       }
    mock_data_user2 = {"name": "user's name2 test_delete_all_user",
                       "email": "test_delete_all_user2@gmail.com",
                       "username": "test_delete_all_user_username2",
                       "password": "123456789",
                       "role": "user",
                       }

    mongo.user.insert_many(documents=[mock_data_user1, mock_data_user2])
    response = client.delete(f'/user')
    assert response.status_code == 200
