import pytest
from pymongo import MongoClient
from app.app import create_app
from app.config.config import TestConfig
from app.util import db as connected_db


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='module')
def mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = connected_db
    yield db
    # client.drop_database('test_elearning_db')