# FactCheck Service

Minimal scaffold for a FastAPI-based fact checking service.

## Local Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

- Health: GET http://localhost:8080/health
- Echo: GET http://localhost:8080/echo?message=hi

## Docker

```bash
docker build -t factcheck-service:local .
docker run -p 8080:8080 factcheck-service:local
```

## Cloud Functions
- cloud_functions/data_fetcher/main.py entry fetch
- cloud_functions/data_indexer/main.py entry index
