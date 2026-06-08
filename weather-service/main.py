from fastapi import FastAPI
from pymongo import MongoClient
import requests
from datetime import datetime

app = FastAPI()

client = MongoClient("mongodb://mongo-db:27017/")
db = client.skyguard_weather


@app.get("/")
def health():
    return {"status": "weather-service OK"}


@app.get("/weather/")
def get_weather():

    url = "https://api.open-meteo.com/v1/forecast?latitude=46.0569&longitude=14.5058&current=temperature_2m,weather_code"

    response = requests.get(url)
    data = response.json()

    temperature = data["current"]["temperature_2m"]
    weather_code = data["current"]["weather_code"]

    log = {
        "event": "weather_fetch",
        "temperature": temperature,
        "weather_code": weather_code,
        "timestamp": str(datetime.now())
    }

    db.logs.insert_one(log)

    return {
        "temperature": temperature,
        "weather_code": weather_code,
        "summary": "Live Open-Meteo data"
    }