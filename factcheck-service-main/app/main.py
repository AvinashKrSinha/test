# app/main.py
import base64
from fastapi import FastAPI, HTTPException
from .config import settings
from .logger import get_logger

# Import your models and services
from .models.request_models import ClaimRequest
from .models.response_models import VerificationResult
from .services import content_fetcher, classifier_router
from .services.rag_pipeline import RAGPipeline

# Import the new routers for community features
from .routers import auth_router, posts_router

# --- Application Setup ---
app = FastAPI()
logger = get_logger()
rag_pipeline = RAGPipeline()

# --- Core Endpoints ---

@app.get("/")
def health_check():
    return {"message": f"FactCheck Service running in project {settings.project_id}"}

@app.post("/verify", response_model=VerificationResult)
async def verify_claim(request: ClaimRequest):
    logger.info("Received request: %s", request.dict())

    if not (request.text or request.url or request.file_content):
        raise HTTPException(status_code=400, detail="No input provided")

    claim_text = ""
    image_bytes = None
    audio_bytes = None

    if request.url:
        claim_text = content_fetcher.fetch_content_from_url(request.url)
        if not claim_text:
            raise HTTPException(status_code=400, detail="Failed to fetch URL content")
    elif request.file_content:
        decoded_bytes = base64.b64decode(request.file_content)
        image_bytes = decoded_bytes
    else:
        claim_text = request.text

    # Note: The classify function in the provided code was synchronous.
    # For a fully async endpoint, this should be made async as well.
    category = classifier_router.classify_claim_with_gemini(claim_text or "[file input]")

    if category == "Live":
        gemini_response = await rag_pipeline.handle_claim(
            claim_text=claim_text,
            image_bytes=image_bytes,
            audio_bytes=audio_bytes
        )
        verification_result = {
            "status": "verified_live",
            "claim": claim_text or "[file input]",
            "evidence": gemini_response,
            "score": 0.9
        }
    else: # Handles "Static", "High-Risk", "Invalid", etc.
        verification_result = {
            "status": "discarded",
            "claim": claim_text or "[file input]",
            "evidence": {"source": f"Claim classified as '{category}', not processed by RAG pipeline."},
            "score": 0.0
        }

    return VerificationResult(**verification_result)

# --- Include Community Feature Routers ---
# This adds all the /auth and /posts endpoints to your application
app.include_router(auth_router.router)
app.include_router(posts_router.router)