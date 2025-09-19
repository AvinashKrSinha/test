# app/clients/speech_to_text.py
import logging
from google.cloud import speech

logger = logging.getLogger("factcheck_service")

class SpeechToTextClient:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio(self, audio_bytes: bytes, language_code: str = "en-US") -> str:
        try:
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code
            )
            response = self.client.recognize(config=config, audio=audio)
            return " ".join([result.alternatives[0].transcript for result in response.results])
        except Exception as e:
            logger.error(f"Speech-to-Text failed: {e}")
            return ""
