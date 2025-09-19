# app/services/rag_pipeline.py
import logging
from google.cloud import aiplatform
from app.config import settings

logger = logging.getLogger("factcheck_service")

# Initialize Vertex AI
aiplatform.init(project=settings.project_id, location=settings.region)

class RAGPipeline:
    def __init__(self):
        self.index = self._get_vector_index()

    def _get_vector_index(self):
        """
        Connect to Vertex AI Vector Search index.
        """
        try:
            index_endpoint = f"projects/{settings.project_id}/locations/{settings.region}/indexes/your-vector-index-id"
            return aiplatform.MatchingEngineIndex(index_endpoint)
        except Exception as e:
            logger.error(f"Failed to connect to Vector Index: {e}")
            return None

    def embed_text(self, text: str):
        """
        Generate embeddings for a given text using Vertex AI Embedding API.
        """
        try:
            embedding_model = aiplatform.TextEmbeddingModel("textembedding-gecko@001")
            embeddings = embedding_model.get_embeddings([text])[0]
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return None

    def search_similar(self, embeddings):
        """
        Search for similar items in Vertex AI Vector Index.
        """
        try:
            if not self.index:
                logger.warning("Vector Index not initialized")
                return []

            response = self.index.match(
                queries=[embeddings],
                num_neighbors=5
            )
            results = []
            for match in response[0].neighbors:
                results.append({
                    "id": match.id,
                    "score": match.distance,
                    "metadata": match.payload
                })
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def generate_augmented_prompt(self, claim_text, search_results):
        """
        Combine claim + retrieved context for Gemini verification.
        """
        context_text = "\n".join([res["metadata"].get("text", "") for res in search_results])
        prompt = f"""
        Verify the following claim using the provided context.
        Claim: {claim_text}
        Context: {context_text}
        Provide a structured JSON with status (verified/false), evidence, and confidence score.
        """
        return prompt

    def verify_with_gemini(self, augmented_prompt):
        """
        Send the enriched prompt to Gemini (via Vertex AI LLM).
        """
        try:
            client = aiplatform.PredictionServiceClient()
            model_name = f"projects/{settings.project_id}/locations/{settings.region}/publishers/google/models/{settings.gemini_model}"
            response = client.predict(
                endpoint=model_name,
                instances=[{"content": augmented_prompt}],
                parameters={}
            )
            return response.predictions[0].get("content", "")
        except Exception as e:
            logger.error(f"Gemini verification failed: {e}")
            return "Error"
