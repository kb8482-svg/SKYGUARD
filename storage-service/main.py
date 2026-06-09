from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from botocore.exceptions import ClientError
import boto3
import io
import time
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


def ensure_bucket():
    for attempt in range(10):
        try:
            s3.head_bucket(Bucket=BUCKET)
            return
        except ClientError as err:
            error_code = err.response.get("Error", {}).get("Code")
            if error_code in ["404", "NoSuchBucket"]:
                s3.create_bucket(Bucket=BUCKET)
                return
            if attempt == 9:
                raise
        except Exception:
            if attempt == 9:
                raise

        time.sleep(2)


@app.on_event("startup")
def startup():
    ensure_bucket()


@app.get("/")
def root():
    return {"status": "storage OK"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):

    ensure_bucket()
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}-{file.filename}"

    content = await file.read()

    s3.put_object(
        Bucket=BUCKET,
        Key=file_name,
        Body=content,
        ContentType=file.content_type or "application/octet-stream"
    )

    url = f"/storage/image/{file_name}"

    return {
        "message": "upload OK",
        "key": file_name,
        "url": url
    }


@app.get("/image/{key}")
def image(key: str):
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
    except ClientError:
        raise HTTPException(status_code=404, detail="Datoteka ne obstaja")

    return StreamingResponse(
        io.BytesIO(obj["Body"].read()),
        media_type=obj.get("ContentType") or "application/octet-stream"
    )
