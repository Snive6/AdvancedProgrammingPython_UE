from fastapi import FastAPI, HTTPException
import json
import pymongo
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["ue_project_1"]
collection = db["ue_project_collection"]

@app.post("/api/results/")
async def receive_results(results: dict):
    try:
        collection.insert_one(results)
        return {"message": "Results saved to the database"}
    except:
        raise HTTPException(status_code=500, detail="An error occurred while saving the results to the database")
