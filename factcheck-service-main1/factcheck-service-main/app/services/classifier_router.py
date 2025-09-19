# app/services/classifier_router.py
import logging
from google.cloud import aiplatform
from app.config import settings

logger = logging.getLogger("factcheck_service")

# Initialize Vertex AI with project & region from env
aiplatform.init(project=settings.project_id, location=settings.region)

def classify_claim_with_gemini(claim_text: str) -> str:
    prompt = f"""
    Classify the following claim into one of four categories: Static, Live, High-Risk, Invalid.
    Claim: \"{claim_text}\"
    Provide only the category as output.
    """

    try:
        client = aiplatform.PredictionServiceClient()
        response = client.predict(
            endpoint=f"projects/{settings.project_id}/locations/{settings.region}/publishers/google/models/{settings.gemini_model}",
            instances=[{"content": prompt}],
            parameters={}
        )
        category = response.predictions[0].get("content", "").strip()
        logger.info(f"Claim classified as: {category}")
        return category
    except Exception as e:
        logger.error(f"Gemini classification failed: {e}")
        return "Invalid"
