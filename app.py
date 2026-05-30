from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "nutrition.json")

with open(file_path, "r") as f:
    nutrition_data = json.load(f)

@app.route("/")
def home():
    return "Food Analyzer API Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    food = data.get("food", "").lower().strip()

    # Exact match only
    if food in nutrition_data:
        return jsonify({
            "status": "found",
            "data": nutrition_data[food]
        })

    return jsonify({
        "status": "not_found"
    })

if __name__ == "__main__":
    app.run()
