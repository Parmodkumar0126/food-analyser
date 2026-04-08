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

# Home route
@app.route("/")
def home():
    return "Food Analyzer API Running 🚀"

# API route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    food = data.get("food", "").lower().strip()

    matched_food = None

    # Smart matching
    for key in nutrition_data:
        if food in key or key in food:
            matched_food = key
            break

    if not matched_food:
        return jsonify({
            "status": "not_found"
        })

    result = nutrition_data[matched_food]

    return jsonify({
        "status": "found",
        "data": result
    })

if __name__ == "__main__":
    app.run()
