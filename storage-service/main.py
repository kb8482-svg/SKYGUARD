from fastapi import FastAPI, UploadFile, File
import boto3
import uuid

app = FastAPI()

# MINIO CONFIG (LOCAL DOCKER NETWORK)
MINIO_URL = "http://minio:9000"

ACCESS_KEY = "user-04"
SECRET_KEY = "thestrongestavajePass04"

BUCKET = "skyguard"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="us-east-1"
)


@app.get("/")
def root():
    return {"status": "storage OK"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_name = f"{file_id}-{file.filename}"

    content = await file.read()

    s3.put_object(
        Bucket=BUCKET,
        Key=file_name,
        Body=content
    )

    url = f"{MINIO_URL}/{BUCKET}/{file_name}"

    return {
        "message": "upload OK",
        "url": url
    }