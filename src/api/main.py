from fastapi import FastAPI
from ml_modules.extractive_text_summarizing import summarize
from typing import Optional
from enum import Enum
import uvicorn

app: FastAPI = FastAPI()


class ModelName(str, Enum):
    extractive_summarizer = "extractive_summarizer"
    model2 = "model2"
    model3 = "model3"


@app.get("/get_text")
async def root(text: str, model_name: ModelName, length_of_summarization: Optional[float] = 0.5):
    summarized_text = ''
    match model_name:
        case ModelName.extractive_summarizer:
            summarized_text = summarize(text, length_of_summarization)
        case ModelName.model2:
            # TODO: implement another algorithm
            ...
        case ModelName.model3:
            # TODO: implement another algorithm
            ...
    return summarized_text


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
