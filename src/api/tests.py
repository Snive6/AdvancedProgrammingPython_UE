import pytest
from fastapi.testclient import TestClient
from jwt.exceptions import ExpiredSignatureError, DecodeError
from jwt import decode
from pymongo import MongoClient
from main import app
import jwt


@pytest.fixture()
def client():
    return TestClient(app)


def test_get_summaries_valid_token(client):
    # Create a valid token
    access_token = jwt.encode({"sub": "test"}, "secret", algorithm="HS256")
    # Insert a test summary into the database
    db = MongoClient("mongodb+srv://admin:admin@cluster0.n8heu6j.mongodb.net/?retryWrites=true&w=majority").testdb
    db.summaries.insert_one({"username": "test", "summary": "test summary", "original_text": "test text"})

    response = client.get("/summaries", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == [{"_id": "test_id", "username": "test", "summary": "test summary",
                                "original_text": "test text"}]


def test_get_summaries_invalid_token(client):
    # Create an invalid token
    access_token = "invalid_token"

    response = client.get("/summaries", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}