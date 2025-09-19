import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel
import requests
from bs4 import BeautifulSoup
import json
import traceback

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

PROJECT_ID = "missinformationgenai"
LOCATION = "us-central1"

# -----------------------------
# Initialize Vertex AI safely
# -----------------------------
try:
    # If running locally, you can optionally set ADC via env variable
    # Vertex AI SDK will automatically pick up ADC or Cloud Run service account
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
except Exception as e:
    print(f"!!! ERROR initializing Vertex AI: {e}")
    model = None

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET"])
def serve_index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return "pong"

@app.route("/analyze", methods=["POST"])
def analyze_text():
    if not model:
        return jsonify({"error": "Vertex AI model not initialized"}), 500

    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request: JSON payload with a 'text' key is required."}), 400

    input_text = data["text"]
    text_to_analyze = ""

    # If input is a URL, scrape text
    if input_text.strip().startswith("http"):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(input_text, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            text_to_analyze = soup.get_text(separator=" ", strip=True)
            if not text_to_analyze:
                return jsonify({"error": "Could not extract text from URL."}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to fetch content from URL: {str(e)}"}), 500
    else:
        text_to_analyze = input_text

    prompt = f"""
    You are a "Digital Misinformation Analyst" assistant. Analyze this text for potential misinformation or scams.
    Return a JSON with:
      - verdict (Likely Trustworthy / Potentially Misleading / High Risk of Misinformation)
      - confidence_score (0.0 to 1.0)
      - summary (short explanation)
      - flags (list of technique + explanation)
    Text: "{text_to_analyze}"
    """

    try:
        response = model.generate_content([prompt])
        json_response_text = response.text.strip().replace("```json", "").replace("```", "")
        parsed_json = json.loads(json_response_text)
        return jsonify(parsed_json)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))