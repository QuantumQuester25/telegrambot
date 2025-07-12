from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "9c79690a9dc84a798be00d2d05b31e8d"
API_SECRET = "7174cb58836543bca990e1e94325a93c"
PASSPHRASE = "Shabak123"

@app.route("/verify", methods=["POST"])
def verify_uid():
    data = request.get_json()
    uid = data.get("uid")

    if not uid:
        return jsonify({"success": False, "message": "UID is required"}), 400

    headers = {
        "BF-API-KEY": API_KEY,
        "BF-API-SECRET": API_SECRET,
        "BF-API-PASSPHRASE": PASSPHRASE,
    }

    try:
        import requests
        response = requests.get("https://api.blofin.com/api/v1/affiliate/invitees", headers=headers)
        invitees = response.json().get("data", [])

        for invitee in invitees:
            if str(invitee.get("userId")) == str(uid):
                return jsonify({"success": True, "message": "UID verified ✅"})

        return jsonify({"success": False, "message": "UID not found ❌"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return "🧠 BloFin Bot Backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
