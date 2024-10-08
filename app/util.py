from pymongo import MongoClient, errors


def connect_db(mode=None):
    connection_str = "mongodb://localhost:27017/"
    if mode is None:
        db_name = 'elearning'
    else:
        db_name = 'test_elearning_db'
    try:
        client = MongoClient(connection_str)
        print(f"Connection {db_name} has established succesfully!")
        db = client[db_name]
        return db
    except errors.ConnectionFailure:
        print("Connection is failed")
        return None
    except Exception as e:
        print(f"An unexpected error occured: {e}")


def serialize(data):
    if data is None:
        return None
    data["_id"] = str(data["_id"])
    data["password"] = str(data["password"])
    return data


def serialize_except_pw(data):
    if data is None:
        return None
    data["_id"] = str(data["_id"])
    return data


db = connect_db(mode='TESTING')
