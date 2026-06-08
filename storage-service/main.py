from fastapi import FastAPI
import requests

app = FastAPI()

MINIO_URL = "http://minio:9000"

@app.get("/")
def root():
    return {"status": "storage OK"}

@app.get("/check-minio/")
def check_minio():
    try:
        r = requests.get(MINIO_URL)
        return {"minio": "reachable"}
    except:
        return {"minio": "not reachable"}