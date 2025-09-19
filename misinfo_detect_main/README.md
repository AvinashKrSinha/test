# AI Misinformation Detector

This project is a **Flask-based web app + API** that uses **Google Cloud Vertex AI (Gemini model)** to analyze text or scraped website content for misinformation, scams, or manipulative language.

---

## 📦 Features

- Analyze plain text or URLs
- Frontend (HTML + JS) served by Flask
- Backend API `/analyze` powered by Vertex AI
- Deployable to **Google Cloud Run**
- No API key required (uses Google Cloud service account authentication)

---

## ⚙️ Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Docker](https://docs.docker.com/get-docker/)
- A Google Cloud Project: `missinformationgenai`
  - Vertex AI API enabled
  - Cloud Run enabled
  - Artifact Registry enabled
  - Service account with `roles/aiplatform.user`

---

## 🖥️ Run and Test Locally

### 1. Install dependencies

```bash
git clone https://github.com/0-101/misinfo_detect.git
cd misinfo_detect
pip install -r requirements.txt
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

This sets up Application Default Credentials (ADC) that Vertex AI needs.

### 3. Run Flask locally

```bash
python main.py
```

### 4. Test API

**Health check:**

```bash
curl http://localhost:8080/ping
```

**Analyze endpoint:**

```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a local test for misinformation detection."}'
```

---

## 🐳 Run with Docker Locally

### 1. Build Docker image

```bash
docker build -t misinformation-api .
```

### 2. Run container with credentials

```bash
docker run -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
  -v ~/.config/gcloud/application_default_credentials.json:/app/key.json:ro \
  misinformation-api
```

### 3. Test API

```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Testing from Docker container."}'
```

---

## 🚀 Deploy to Google Cloud Run

### 1. Configure gcloud

```bash
gcloud config set project missinformationgenai
gcloud config set run/region us-central1
```

### 2. Enable required services

```bash
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com
```

### 3. Create Artifact Registry repo (once only)

```bash
gcloud artifacts repositories create misinformation-repo \
    --repository-format=docker \
    --location=us-central1
```

### 4. Build & push Docker image

```bash
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/missinformationgenai/misinformation-repo/misinformation-api
```

### 5. Deploy to Cloud Run

```bash
gcloud run deploy misinformation-api \
  --image us-central1-docker.pkg.dev/missinformationgenai/misinformation-repo/misinformation-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account 1039291526226-compute@developer.gserviceaccount.com
```

### 6. Test deployed service

After deployment, gcloud prints a URL like:

```
https://misinformation-api-abc123-uc.a.run.app
```

**Check health:**

```bash
curl https://misinformation-api-abc123-uc.a.run.app/ping
```

**Analyze text:**

```bash
curl -X POST https://misinformation-api-abc123-uc.a.run.app/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a Cloud Run test for misinformation detection."}'
```

---

## 🔄 Updating the Service

When you modify code:

```bash
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/missinformationgenai/misinformation-repo/misinformation-api

gcloud run deploy misinformation-api \
  --image us-central1-docker.pkg.dev/missinformationgenai/misinformation-repo/misinformation-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## ✅ API Routes

- **GET /ping** → Health check (returns "pong")
- **POST /analyze** → Analyze text or URL

**Request format:**

```json
{
  "text": "Example text to check"
}
```

---

## 🛡️ Security Notes

- Do not hardcode credentials in code
- **Locally:** use `gcloud auth application-default login`
- **On Cloud Run:** use a service account with `roles/aiplatform.user`

---