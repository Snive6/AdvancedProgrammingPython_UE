import pymongo
from fastapi.testclient import TestClient
from main import create_test_user, pwd_context
from main import app
import jwt
from ml_modules.pegasus import pegasus_summarizer
from ml_modules.extractive_text_summarizing import extractive_summarizer
from ml_modules.bart import bart_summarizer
from main import get_db
import uvicorn


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


client = TestClient(app)


def test_login():
    response = client.post("/login?username=test&password=test")
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    access_token = json_response["access_token"]
    payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
    assert payload["sub"] == "test"
    assert "exp" in payload


def test_get_summaries():
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


def test_summarize():
    # First, create a test user and log in to get an access token
    test_user = {"username": "test", "password": pwd_context.hash("test")}
    db = get_db()
    user_collection = db["users"]
    user_collection.insert_one(test_user)
    login_response = client.post("/login?username=test&password=test")
    access_token = login_response.json()["access_token"]

    # Now, call the /summarize endpoint with a test text and model name
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, " \
           "dignissim sit amet, adipiscing nec, ultricies sed, dolor."
    response = client.get("/summarize", params={"text": text, "model_name": "extractive_summarizer",
                                                "access_token": access_token})
    assert response.status_code == 200
    json_response = response.json()
    assert "summary" in json_response

    # Check if the summary was saved in the database
    collection = db["summaries"]
    summary = collection.find({'username': 'test'}).sort([("_id", pymongo.DESCENDING)]).limit(1)[0]
    assert summary["summary"] == json_response["summary"]
    assert summary["original_text"] == text


if __name__ == '__main__':
    db = get_db()
    create_test_user(db)
    uvicorn.run('main:app', reload=True)
