from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("BLOFIN_API_KEY")
API_SECRET = os.getenv("BLOFIN_API_SECRET")
PASSPHRASE = os.getenv("BLOFIN_PASSPHRASE")

@app.route('/verify', methods=['POST'])
def verify_uid():
    data = request.get_json()
    uid = str(data.get("uid"))

    if not uid:
        return jsonify({"success": False, "error": "UID not provided"}), 400

    try:
        import requests
        headers = {
            "Content-Type": "application/json",
            "BF-API-KEY": API_KEY,
            "BF-API-SECRET": API_SECRET,
            "BF-API-PASSPHRASE": PASSPHRASE
        }

        response = requests.get("https://api.blofin.com/api/v1/affiliate/invitees", headers=headers)
        invitees = response.json().get("data", [])

        for user in invitees:
            if str(user.get("userId")) == uid:
                return jsonify({"success": True, "message": "UID verified"}), 200

        return jsonify({"success": False, "message": "UID not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
