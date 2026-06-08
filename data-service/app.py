from fastapi import FastAPI
import os

app = FastAPI(title="SKYGUARD Data Service")

@app.get("/api/data/health")
def health_check():
    return {"status": "Data service is running", "database": "MongoDB"}

@app.get("/api/data/status")
def get_status():
    return {"status": "Vse sistemske komponente SKYGUARD delujejo optimalno."}