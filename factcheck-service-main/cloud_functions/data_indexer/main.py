# cloud_functions/data_indexer/main.py
import os
import json
from google.cloud import storage
from app.clients.vertex_ai import VertexAIClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

INDEX_ENDPOINT_ID = os.environ.get("INDEX_ENDPOINT_ID")

storage_client = storage.Client()
vertex_client = VertexAIClient()

def index_file(event, context):
    bucket_name = event['bucket']
    file_name = event['name']
    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()

    try:
        articles = json.loads(content)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return

    texts_to_embed = []
    metadata_list = []
    ids_list = []

    for idx, article in enumerate(articles):
        text_content = article.get("content", "")
        if text_content.strip():
            texts_to_embed.append(text_content)
            metadata_list.append({"source": str(article.get("source", ""))})
            ids_list.append(f"{file_name}-{idx}")

    if not texts_to_embed:
        print("No content found to index.")
        return

    print(f"Generating embeddings for {len(texts_to_embed)} articles...")
    embeddings = vertex_client.generate_embeddings(texts_to_embed)

    print(f"Upserting {len(embeddings)} vectors to Vertex AI Vector Search...")
    # The 'deployed_index_id' argument has been removed from this call
    vertex_client.upsert_vectors(
        embeddings=embeddings,
        metadata_list=metadata_list,
        ids=ids_list,
        index_endpoint_id=INDEX_ENDPOINT_ID
    )

    print(f"Successfully indexed {len(embeddings)} articles from {file_name}")