from fastapi import FastAPI
from pymongo import MongoClient
import requests
from datetime import datetime

app = FastAPI()

client = MongoClient("mongodb://mongo-db:27017/")
db = client.skyguard_weather

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LATITUDE = 46.0569
DEFAULT_LONGITUDE = 14.5058

WEATHER_SUMMARIES = {
    0: "Jasno",
    1: "Delno oblačno",
    2: "Oblačno",
    3: "Zelo oblačno",
    45: "Megleno",
    48: "Megleno z rosno meglico",
    51: "Lahek dež",
    53: "Zmeren dež",
    55: "Močan dež",
    56: "Lahek zamrznjen dež",
    57: "Močan zamrznjen dež",
    61: "Dež",
    63: "Zmeren dež",
    65: "Intenziven dež",
    66: "Lahek sneg",
    67: "Močan sneg",
    71: "Sneženje",
    73: "Zmerno sneženje",
    75: "Močno sneženje",
    77: "Snežni kristali",
    80: "Pljuski",
    81: "Močni pljuski",
    82: "Zelo močni pljuski",
    85: "Snežni pljuski",
    86: "Močni snežni pljuski",
    95: "Nevihte",
    96: "Nevihta s točo",
    99: "Močna nevihta s točo"
}


def get_weather_description(code: int):
    return WEATHER_SUMMARIES.get(code, "Neznano vreme")


@app.get("/")
def health():
    return {"status": "weather-service OK"}


@app.get("/weather/")
@app.get("/weather/current")
def get_weather(latitude: float = DEFAULT_LATITUDE, longitude: float = DEFAULT_LONGITUDE):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "relativehumidity_2m,precipitation_probability,precipitation",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 4,
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current_weather", {})
    temperature = current.get("temperature")
    weather_code = current.get("weathercode")
    wind_speed = current.get("windspeed")
    weather_time = current.get("time")

    humidity = None
    rain_chance = None
    precipitation = None

    if weather_time and "hourly" in data:
        hourly = data["hourly"]
        if weather_time in hourly.get("time", []):
            index = hourly["time"].index(weather_time)
            humidity = hourly.get("relativehumidity_2m", [None])[index]
            rain_chance = hourly.get("precipitation_probability", [None])[index]
            precipitation = hourly.get("precipitation", [None])[index]

    forecast = []
    daily = data.get("daily", {})
    if daily:
        count = min(3, len(daily.get("time", [])))
        for index in range(count):
            forecast.append({
                "date": daily["time"][index],
                "weather_code": daily["weather_code"][index],
                "temperature_min": daily["temperature_2m_min"][index],
                "temperature_max": daily["temperature_2m_max"][index],
                "precipitation_probability": daily["precipitation_probability_max"][index],
            })

    radar_url = None
    try:
        radar_url = f"https://api.open-meteo.com/v1/radar?latitude={latitude}&longitude={longitude}&radar_format=png"
    except Exception:
        radar_url = None

    log = {
        "event": "weather_fetch",
        "latitude": latitude,
        "longitude": longitude,
        "temperature": temperature,
        "weather_code": weather_code,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "rain_chance": rain_chance,
        "timestamp": str(datetime.now())
    }

    db.logs.insert_one(log)

    return {
        "temperature": temperature,
        "weather_code": weather_code,
        "weather_summary": get_weather_description(weather_code) if weather_code is not None else "Neznano vreme",
        "wind_speed": wind_speed,
        "humidity": humidity,
        "rain_chance": rain_chance,
        "precipitation": precipitation,
        "forecast": forecast,
        "radar_image_url": radar_url,
    }


@app.get("/weather/forecast")
def get_forecast(latitude: float = DEFAULT_LATITUDE, longitude: float = DEFAULT_LONGITUDE):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 5,
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    daily = response.json()["daily"]

    forecast = [
        {
            "date": daily["time"][index],
            "weather_code": daily["weather_code"][index],
            "temperature_min": daily["temperature_2m_min"][index],
            "temperature_max": daily["temperature_2m_max"][index],
            "precipitation_probability": daily["precipitation_probability_max"][index],
        }
        for index in range(len(daily["time"]))
    ]

    db.logs.insert_one({
        "event": "forecast_fetch",
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": str(datetime.now())
    })

    return {"forecast": forecast}


@app.get("/weather/alerts")
def get_alerts(latitude: float = DEFAULT_LATITUDE, longitude: float = DEFAULT_LONGITUDE):
    current = get_weather(latitude, longitude)
    alerts = []

    if current["wind_speed"] is not None and current["wind_speed"] >= 40:
        alerts.append("Močan veter lahko ogrozi dogodke na prostem.")
    if current["weather_code"] in [61, 63, 65, 80, 81, 82, 95, 96, 99]:
        alerts.append("Napovedane so padavine ali nevihta.")

    return {"alerts": alerts, "safe_for_outdoor_event": len(alerts) == 0}
