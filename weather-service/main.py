from fastapi import FastAPI

app = FastAPI()

@app.get("/current")
def get_current():
    return {"location": "Ljubljana", "temperature": "18°C", "condition": "Pretežno oblačno"}

@app.get("/forecast")
def get_forecast():
    return {"forecast": [{"day": "Jutri", "temp": "21°C", "condition": "Sončno"}]}

@app.get("/alerts")
def get_alerts():
    return {"alerts": []}