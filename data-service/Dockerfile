FROM python:3.12-slim
WORKDIR /app
RUN pip install fastapi uvicorn pymongo
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5002"]