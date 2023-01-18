import os
import spacy
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
import jwt
from ml_modules.pegasus import PegasusSummarizer
from ml_modules.extractive_summarizer_model import extractive_summarizer
from ml_modules.bart import BartSummarizer

from src.api.const import JWT_SECRET_KEY

load_dotenv()


def test_summarizer():
    summarizer = BartSummarizer()
    text = open("ml_modules/example/text_example.txt", "r").read()
    expected_summary = ' Machine learning (ML) is the scientific study of algorithms and statistical ' \
                       'models that computer systems use to progressively improve their performance ' \
                       'on a specific task . Machine learning algorithms are used in the ' \
                       'applications of email filtering, detection of network intruders, and ' \
                       'computer vision, where it is infeasible to'
    summary = summarizer.summarize(text, max_length=60)
    assert summary == expected_summary


def test_extractive_summarizer():
    nlp = spacy.load('en_core_web_sm')
    text = open("ml_modules/example/text_example.txt", "r").read()
    per = 0.5
    expected_summary = "Machine learning algorithms are used in the applications of email filtering, detection of " \
                       "network intruders, and computer vision, where it is infeasible to develop an algorithm of " \
                       "specific instructions for performing the task.Machine learning algorithms build a " \
                       "mathematical model of sample data, known as â€śtraining dataâ€ť, in order to make predictions" \
                       " or decisions without being explicitly programmed to perform the task.The study of " \
                       "mathematical optimization delivers methods, theory and application domains to the " \
                       "field of machine learning."

    summary = extractive_summarizer(text, per, nlp)
    assert summary == expected_summary


def test_pegasus_summarizer():
    summarizer = PegasusSummarizer()
    text = open("ml_modules/example/text_example.txt", "r").read()
    # expected_summary = 'Machine learning algorithms are used in the applications of email filtering, detection of ' \
    #                    'network intruders, and computer vision, where it is infeasible to develop an algorithm of ' \
    #                    'specific instructions for performing the task.'

    expected_summary = 'The global machine learning research and development (R&D) research and ' \
                       'development (R&D) research and development (R&D) research and development ' \
                       '(R&D) research and development (R&D) research and development (R&D) research ' \
                       'and development (R&D'
    max_length = 60

    summary = summarizer.summarize(text, max_length)
    assert summary == [expected_summary]


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_login(client):
    response = client.post("/login?username=test&password=test")
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    access_token = json_response["access_token"]
    payload = jwt.decode(access_token, str(os.getenv(JWT_SECRET_KEY)), algorithms=["HS256"])
    assert payload["sub"] == "test"
    assert "exp" in payload


def test_get_summaries(client):
    # First, login to get an access token
    login_response = client.post("/login?username=test&password=test")
    json_response = login_response.json()
    access_token = json_response["access_token"]

    # Now, call the /summaries endpoint with the access token
    response = client.get(f"summaries?access_token={access_token}")

    # Assert that the response has a status code of 200 OK
    assert response.status_code == 200

    # Assert that the response body contains the expected data
    json_response = response.json()
    assert isinstance(json_response, list)
    assert all(isinstance(summary, dict) for summary in json_response)
    assert all("_id" in summary for summary in json_response)
    assert all("username" in summary for summary in json_response)
    assert all("summary" in summary for summary in json_response)
    assert all("original_text" in summary for summary in json_response)


def test_summarize(client):
    valid_token = jwt.encode({"sub": "test"}, str(os.getenv(JWT_SECRET_KEY)), algorithm="HS256")
    invalid_token = jwt.encode({"sub": "invalid_user"}, 'not_secret_key', algorithm="HS256")
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
           "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip " \
           "ex ea commodo consequat."

    # Test valid token
    response = client.get("/summarize?text={}&model_name={}&access_token={}".format(text, "extractive_summarizer",
                                                                                    valid_token))
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"] is not None
    assert len(response.json()["summary"]) > 0

    # Test invalid token
    response = client.get("/summarize?text={}&model_name={}&access_token={}".format(text, "extractive_summarizer",
                                                                                    invalid_token))
    assert response.status_code == 401
    assert "detail" in response.json() and response.json()["detail"] == "Invalid token"
