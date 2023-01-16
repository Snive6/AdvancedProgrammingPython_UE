from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from ml_modules.extractive_text_summarizing import extractive_summarizer as default_summarizer
from ml_modules.pegasus import pegasus_summarizer
from ml_modules.bart import bart_summarizer
from typing import Optional
from enum import Enum
import uvicorn
from pymongo import MongoClient
import jwt
import time
from passlib.context import CryptContext
import os

from src.api.const import (
    MONGO_URL,
    MONGO_DATABASE_NAME,
    MONGO_COLLECTION_NAME_USERS,
    MONGO_COLLECTION_NAME_SUMMARIES,
    JWT_SECRET_KEY,
)

load_dotenv()


app = FastAPI()

# Create a password context object to handle password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency function to get database connection
def get_db():
    client = MongoClient(str(os.getenv(MONGO_URL)))
    # db = client.test
    db = client[str(os.getenv(MONGO_DATABASE_NAME))]
    return db


def create_test_user(db):
    hashed_password = pwd_context.hash("test")
    test_user = {"username": "test", "password": hashed_password}
    user_collection = db[str(os.getenv(MONGO_COLLECTION_NAME_USERS))]
    user_collection.insert_one(test_user)


@app.on_event("startup")
async def startup():
    db = get_db()
    create_test_user(db)


# Function to authenticate a user by checking their username and password
async def authenticate_user(username: str, password: str):
    db = get_db()
    user_collection = db[str(os.getenv(MONGO_COLLECTION_NAME_USERS))]
    user = user_collection.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return user


# Login endpoint
@app.post("/login", status_code=status.HTTP_200_OK)
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    # Create a JWT token that contains the user's username and expires in 15 minutes
    access_token = jwt.encode({"sub": user["username"], "exp": int(time.time() + 900)},
                              str(os.getenv(JWT_SECRET_KEY)), algorithm="HS256")

    return {"access_token": access_token}


@app.post("/logout")
async def logout():
    return {"message": "User has been logged out"}


class ModelName(str, Enum):
    extractive_summarizer = "extractive_summarizer"
    pegasus = "pegasus"
    bart = "bart"


responses = {
    408: {"description": "Request Timeout"},
    429: {"description": "Too many requests"},
    500: {"description": "Internal Server Error"},
}


@app.get("/summarize", status_code=status.HTTP_200_OK,
         responses={**responses})
async def root(text: str, model_name: ModelName, access_token, db: MongoClient = Depends(get_db),
               length_of_summarization: Optional[float] = 0.6):
    try:
        payload = jwt.decode(access_token, str(os.getenv(JWT_SECRET_KEY)), algorithms=["HS256"])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")

    summarized_text = ''
    match model_name:
        case ModelName.extractive_summarizer:
            summarized_text = default_summarizer(text, length_of_summarization)
        case ModelName.pegasus:
            summarized_text = pegasus_summarizer(text, max_length=length_of_summarization * 100)[0]
        case ModelName.bart:
            summarized_text = bart_summarizer(text, max_length=length_of_summarization * 100)

    # Save the summary and original text to the database
    collection = db[MONGO_COLLECTION_NAME_SUMMARIES]

    try:
        collection.insert_one({"summary": summarized_text, "original_text": text, "username": username})
    except:
        raise HTTPException(status_code=500, detail="An error occurred while saving the results to the database")

    return {"summary": summarized_text}


@app.get("/summaries", status_code=status.HTTP_200_OK,
         responses={**responses})
async def get_summaries(access_token: str):
    db = get_db()
    try:
        payload = jwt.decode(access_token, str(os.getenv(JWT_SECRET_KEY)), algorithms=["HS256"])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    # Find all summaries for the current user in the database
    collection = db[str(os.getenv(MONGO_COLLECTION_NAME_SUMMARIES))]
    summaries = collection.find({"username": username})
    return [{"_id": str(summary["_id"]), "username": summary["username"], "summary": summary["summary"],
             "original_text": summary["original_text"]} for summary in summaries]


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
