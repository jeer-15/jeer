# Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "rag_query.py"]  # Or uvicorn rag_query:app --host 0.0.0.0 --port 8080 if using FastAPI