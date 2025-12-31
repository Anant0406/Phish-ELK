# save as mock_api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/quarantine", methods=["POST"])
def quarantine():
    data = request.get_json()
    print(f"Quarantined email: {data}")
    return jsonify({"status": "success", "message": "Email quarantined"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
