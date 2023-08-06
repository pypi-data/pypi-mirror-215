import json
from flask import request, Flask

from sap_aicore_llm.qa_retrieval import RetrievalManager

retriever = RetrievalManager()

app = Flask(__name__)


@app.after_request
def apply_security_headers(response):
    headers = get_security_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response


def get_security_headers():
    headers = {
        "Content-Type": "application/json",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "X-Content-Security-Policy": "default-src 'self'",
        "X-Content-Type-Options": "nosniff"
    }
    return headers


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for errors."""
    response = {
        "status_code": 500,
        "error": f"{type(e).__name__}: {str(e)}"
    }

    response_data = sanitize_json(json.dumps(response))
    return response_data, 500, get_security_headers()


def sanitize_json(json_string):
    s = json_string.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s


@app.route("/v1/query", methods=["POST"])
def query():
    user_query = request.get_json().get("query")

    result = retriever.handle_query(user_query)
    result = json.dumps(result)
    return result, 200


@app.get("/v1/healthz")
def health():
    return "OK", 200
