from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from google.cloud.aiplatform_v1.types import IndexDatapoint
import os

class VertexAIClient:
    def __init__(self):
        project = os.environ.get("PROJECT_ID")
        region = os.environ.get("REGION", "us-central1")
        aiplatform.init(project=project, location=region)
        self.model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    def generate_embeddings(self, texts: list):
        if not texts:
            return []
        response = self.model.get_embeddings(texts)
        return [embedding.values for embedding in response]

    def upsert_vectors(self, embeddings: list, metadata_list: list, ids: list, index_endpoint_id: str):
        full_endpoint_name = (
            f"projects/{os.environ.get('PROJECT_ID')}/locations/"
            f"{os.environ.get('REGION', 'us-central1')}/indexEndpoints/{index_endpoint_id}"
        )
        index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=full_endpoint_name)

        datapoints = [
            IndexDatapoint(
                datapoint_id=id,
                feature_vector=vector,
                restricts=[
                    IndexDatapoint.Restriction(
                        namespace=key, allow_list=[str(value)]
                    ) for key, value in metadata.items()
                ]
            )
            for id, vector, metadata in zip(ids, embeddings, metadata_list)
        ]

        # Upsert on the Index resource, not the Endpoint
        gca = getattr(index_endpoint, "gca_resource", None)
        deployed_indexes = gca.deployed_indexes if gca and hasattr(gca, "deployed_indexes") else []
        if not deployed_indexes:
            raise RuntimeError("No deployed indexes found on the specified Index Endpoint")

        index_resource_name = deployed_indexes[0].index
        index = aiplatform.MatchingEngineIndex(index_name=index_resource_name)
        index.upsert_datapoints(datapoints=datapoints)

    def search_vectors(self, query_embedding: list, index_endpoint_id: str, num_neighbors: int = 5):
        full_endpoint_name = (
            f"projects/{os.environ.get('PROJECT_ID')}/locations/"
            f"{os.environ.get('REGION', 'us-central1')}/indexEndpoints/{index_endpoint_id}"
        )
        index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=full_endpoint_name)

        # Get deployed index id for querying
        gca = getattr(index_endpoint, "gca_resource", None)
        deployed_indexes = gca.deployed_indexes if gca and hasattr(gca, "deployed_indexes") else []
        if not deployed_indexes:
            raise RuntimeError("No deployed indexes found on the specified Index Endpoint")
        deployed_index_id = deployed_indexes[0].id

        response = index_endpoint.find_neighbors(
            queries=[query_embedding],
            deployed_index_id=deployed_index_id,
            num_neighbors=num_neighbors,
            return_full_datapoint=True
        )
        
        neighbors = []
        if response and response[0]:
            for neighbor in response[0].neighbors if hasattr(response[0], "neighbors") else response[0]:
                # Handle both shapes: neighbor.id or neighbor.datapoint.datapoint_id
                neighbor_id = getattr(neighbor, "id", None)
                if not neighbor_id and hasattr(neighbor, "datapoint") and hasattr(neighbor.datapoint, "datapoint_id"):
                    neighbor_id = neighbor.datapoint.datapoint_id

                # Extract metadata from datapoint.restricts if available
                restricts = []
                if hasattr(neighbor, "datapoint") and hasattr(neighbor.datapoint, "restricts"):
                    restricts = neighbor.datapoint.restricts or []

                metadata = {r.namespace: (r.allow_list[0] if getattr(r, "allow_list", []) else "") for r in restricts}

                neighbors.append({
                    "id": neighbor_id,
                    "distance": getattr(neighbor, "distance", None),
                    "metadata": metadata
                })

        return neighbors