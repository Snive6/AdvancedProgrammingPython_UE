from fastapi import FastAPI
from ml_modules.extractive_text_summarizing import summarize

app: FastAPI = FastAPI()


@app.get("/get_text")
async def root(text: str, length_of_summarization: float):
    summarized_text = summarize(text)
    return summarized_text

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
