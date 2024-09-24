import pytest
from pymongo import MongoClient
from app.app import create_app
from app.config.config import TestConfig


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='module')
def mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_elearning_db
    yield db
    # client.drop_database('test_elearning_db')
