# app/services/classifier_router.py
import logging
from google.cloud.aiplatform.gapic.v1 import PredictionServiceClient
from google.api_core import client_options
from app.config import settings

logger = logging.getLogger("factcheck_service")

# Define the regional endpoint for the API call
client_options = client_options.ClientOptions(
    api_endpoint=f"{settings.region}-aiplatform.googleapis.com"
)

# Create the client once with the specified endpoint
client = PredictionServiceClient(client_options=client_options)

def classify_claim_with_gemini(claim_text: str) -> str:
    prompt = f"""
    Classify the following claim into one of four categories: Static, Live, High-Risk, Invalid.
    Claim: \"{claim_text}\"
    Provide only the category as output.
    """

    try:
        # Construct the full model endpoint path
        endpoint_path = f"projects/{settings.project_id}/locations/{settings.region}/publishers/google/models/{settings.gemini_model}"

        # Use the pre-initialized client
        response = client.predict(
            endpoint=endpoint_path,
            instances=[{"content": prompt}],
            parameters={}
        )
        category = response.predictions[0].get("content", "").strip()
        logger.info(f"Claim classified as: {category}")
        return category
    except Exception as e:
        logger.error(f"Gemini classification failed: {e}")
        return "Invalid"