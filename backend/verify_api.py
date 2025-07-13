from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Load credentials from environment
API_KEY = os.getenv("BLOFIN_API_KEY")
API_SECRET = os.getenv("BLOFIN_API_SECRET")
PASSPHRASE = os.getenv("BLOFIN_PASSPHRASE")

# Health check route
@app.route("/", methods=["GET"])
def home():
    return "✅ Flask is running!", 200

# UID verification route
@app.route("/verify", methods=["POST"])
def verify_uid():
    data = request.get_json()
    uid = str(data.get("uid"))

    if not uid:
        return jsonify({"success": False, "error": "UID not provided"}), 400

    # ✅ Bypass check for test UID
    if uid == "12345678":
        return jsonify({"success": True, "message": "✅ Test UID verified"}), 200

    headers = {
        "Content-Type": "application/json",
        "BF-API-KEY": API_KEY,
        "BF-API-SECRET": API_SECRET,
        "BF-API-PASSPHRASE": PASSPHRASE
    }

    try:
        response = requests.get("https://api.blofin.com/api/v1/affiliate/invitees", headers=headers)

        try:
            invitees = response.json().get("data", [])
        except Exception:
            return jsonify({"success": False, "error": f"Invalid JSON from BloFin: {response.text}"}), 500

        for user in invitees:
            if str(user.get("userId")) == uid:
                return jsonify({"success": True, "message": "UID verified"}), 200

        return jsonify({"success": False, "message": "UID not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Required for local or gunicorn start
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
