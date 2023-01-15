import pytest
from fastapi.testclient import TestClient
from jwt.exceptions import ExpiredSignatureError, DecodeError
from jwt import decode
from pymongo import MongoClient
from main import app
import jwt
from ml_modules.pegasus import pegasus_summarizer
from ml_modules.extractive_text_summarizing import extractive_summarizer
from ml_modules.bart import bart_summarizer


def test_bart_summarizer():
    text = open("ml_modules/example/text_example", "r").read()
    expected_summary = ' Machine learning (ML) is the scientific study of algorithms and statistical models that ' \
                       'computer systems use to progressively improve their performance on a specific task . ' \
                       'Machine learning algorithms are used in the applications of email filtering, detection ' \
                       'of network intruders, and computer vision, where it is infeasible to develop an algorithm ' \
                       'of specific instructions for performing the task .'
    max_length = 100

    summary = bart_summarizer(text, max_length)
    assert summary == expected_summary


def test_extractive_summarizer():
    text = open("ml_modules/example/text_example", "r").read()
    per = 0.5
    expected_summary = "Machine learning algorithms are used in the applications of email filtering, detection of " \
                       "network intruders, and computer vision, where it is infeasible to develop an algorithm of " \
                       "specific instructions for performing the task.Machine learning algorithms build a " \
                       "mathematical model of sample data, known as â€śtraining dataâ€ť, in order to make predictions" \
                       " or decisions without being explicitly programmed to perform the task.The study of " \
                       "mathematical optimization delivers methods, theory and application domains to the " \
                       "field of machine learning."

    summary = extractive_summarizer(text, per)
    assert summary == expected_summary


def test_pegasus_summarizer():
    text = open("ml_modules/example/text_example", "r").read()
    expected_summary = 'Machine learning algorithms are used in the applications of email filtering, detection of ' \
                       'network intruders, and computer vision, where it is infeasible to develop an algorithm of ' \
                       'specific instructions for performing the task.'
    max_length = 100

    summary = pegasus_summarizer(text, max_length)
    assert summary == [expected_summary]


@pytest.fixture()
def client():
    return TestClient(app)


# TODO: complete it. Returns status 422
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


# TODO: complete it. Returns status 422
def test_get_summaries_invalid_token(client):
    # Create an invalid token
    access_token = "invalid_token"

    response = client.get("/summaries", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
