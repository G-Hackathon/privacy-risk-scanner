from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze
from datetime import datetime

app = Flask(__name__)
CORS(app)

APP_NAME = "Privacy Risk Scanner"
VERSION = "3.0.0"


@app.route("/")
def home():
    return jsonify({
        "name": APP_NAME,
        "version": VERSION,
        "status": "online",
        "message": "Privacy Risk Scanner API is running.",
        "endpoints": [
            "/",
            "/health",
            "/scan"
        ]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": VERSION
    })


@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Missing JSON body."
        }), 400

    if "url" not in data:
        return jsonify({
            "success": False,
            "error": "URL not provided."
        }), 400

    url = data["url"].strip()

    if url == "":
        return jsonify({
            "success": False,
            "error": "URL is empty."
        }), 400

    if not (
        url.startswith("http://")
        or
        url.startswith("https://")
    ):
        return jsonify({
            "success": False,
            "error": "URL must begin with http:// or https://"
        }), 400

    try:

        result = analyze(url)

        result["success"] = True
        result["scan_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result["version"] = VERSION

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
