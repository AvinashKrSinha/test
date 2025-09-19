# local_test.py
import os
from cloud_functions.data_indexer.main import index_file

def run_test():
    # Ensure the PROJECT_ID is set, as the client needs it.
    if not os.environ.get("PROJECT_ID"):
        print("Error: PROJECT_ID environment variable not set.")
        return

    if not os.environ.get("GCS_BUCKET"):
        print("Error: GCS_BUCKET environment variable not set.")
        return

    # 1. Define the mock event dictionary.
    # This simulates the data that GCS sends to your function.
    mock_event = {
        "bucket": os.environ.get("GCS_BUCKET"),
        "name": "sample_article.json"  # Must exist in the bucket
    }

    # 2. The 'context' object is not used in your function, so we can pass None.
    mock_context = None

    print("--- Starting local function test ---")
    try:
        # 3. Call the function directly.
        index_file(mock_event, mock_context)
        print("--- Function execution finished successfully ---")
    except Exception as e:
        print(f"--- Function execution failed: {e} ---")
        # Optionally print the full traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()