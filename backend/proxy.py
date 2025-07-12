from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

BLOFIN_API_URL = "https://blofin.com/api/user/api/get-user-uid"
HEADERS = {
    "authority": "blofin.com",
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": "https://blofin.com",
    "referer": "https://blofin.com/",
    "user-agent": "Mozilla/5.0",
}
API_KEY = os.getenv("BLOFIN_API_KEY")  # Optional: if needed

@app.route("/verify", methods=["POST"])
def verify_uid():
    try:
        data = request.get_json()
        uid = data.get("uid")
        if not uid:
            return jsonify({"error": "UID is required"}), 400

        response = requests.post(BLOFIN_API_URL, json={"uid": uid}, headers=HEADERS)

        # If response is not JSON, send plain text or HTML back
        try:
            return jsonify(response.json())
        except Exception:
            return jsonify({"error": "Non-JSON response", "raw": response.text}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
