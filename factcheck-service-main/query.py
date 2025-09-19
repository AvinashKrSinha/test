import os
from app.clients.vertex_ai import VertexAIClient
from dotenv import load_dotenv


load_dotenv() 
vertex_client = VertexAIClient()

query_text = "Where is the Eiffel Tower?"
embedding = vertex_client.generate_embeddings([query_text])[0]

results = vertex_client.search_vectors(embedding, index_endpoint_id=os.environ["INDEX_ENDPOINT_ID"], num_neighbors=10)

print("Search results:")
for res in results:
    print(f"ID: {res['id']}, Distance: {res['distance']}, Metadata: {res['metadata']}")
