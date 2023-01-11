from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ml_modules.extractive_text_summarizing import summarize as default_summarizer
from ml_modules.pegasus import pegasus_summarizer
from ml_modules.bart_summarizer import bart_summarizer
from typing import Optional
from enum import Enum
import uvicorn

app: FastAPI = FastAPI()
security = HTTPBasic()

users = {"trudnY": "PaC13Nt"}


@app.post("/login/")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = users.get(credentials.username)
    if correct_username is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if correct_username != credentials.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Welcome"}


class ModelName(str, Enum):
    extractive_summarizer = "extractive_summarizer"
    pegasus = "pegasus"
    bart = "bart"


responses = {
    408: {"description": "Request Timeout"},
    429: {"description": "Too many requests"},
    500: {"description": "Internal Server Error"},
}


@app.get("/get_text", status_code=status.HTTP_200_OK,
         responses={**responses})
async def root(text: str, model_name: ModelName, length_of_summarization: Optional[float] = 0.6):
    summarized_text = ''
    match model_name:
        case ModelName.extractive_summarizer:
            summarized_text = default_summarizer(text, length_of_summarization)
        case ModelName.pegasus:
            summarized_text = pegasus_summarizer(text, max_length=length_of_summarization*100)[0]
        case ModelName.bart:
            summarized_text = bart_summarizer(text, max_length=length_of_summarization*100)
    return summarized_text


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
