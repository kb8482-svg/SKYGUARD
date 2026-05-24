from fastapi import FastAPI
import urllib.request
import json

app = FastAPI()

@app.get("/current")
def get_current_weather(latitude: float = 46.0569, longitude: float = 14.5058):
    """
    Pridobiva real-time vremenske podatke. 
    Če koordinat ni, avtomatsko izbere Ljubljano (46.0569, 14.5058).
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            current = data.get("current_weather", {})
            
            return {
                "status": "success",
                "mesto": "Ljubljana (Privzeto)" if latitude == 46.0569 else "Izbrane koordinate",
                "koordinate": {"lat": latitude, "lon": longitude},
                "vreme_v_realnem_casu": {
                    "temperatura": f"{current.get('temperature')}°C",
                    "hitrost_vetra": f"{current.get('windspeed')} km/h",
                    "osveženo": current.get("time")
                }
            }
    except Exception as e:
        return {"status": "error", "message": f"Napaka pri pridobivanju podatkov: {str(e)}"}