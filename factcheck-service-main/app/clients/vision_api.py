# app/clients/vision_api.py
import logging
from google.cloud import vision

logger = logging.getLogger("factcheck_service")

class VisionAPIClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        try:
            image = vision.Image(content=image_bytes)
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            return texts[0].description if texts else ""
        except Exception as e:
            logger.error(f"Vision API OCR failed: {e}")
            return ""
