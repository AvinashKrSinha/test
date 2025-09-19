def format_response(verdict: str, confidence: float, rationale: str) -> dict:
    return {"verdict": verdict, "confidence": confidence, "rationale": rationale}


