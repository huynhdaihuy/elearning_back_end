from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB')


def connect_db(mongo_url, db_name):
    try:
        client = MongoClient(mongo_url)
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

db = connect_db(mongo_uri,db_name)