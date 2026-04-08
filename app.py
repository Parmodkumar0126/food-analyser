from flask import Flask, render_template, request
from clarifai.client.model import Model
import json

# 🔑 API KEY
PAT = "bd5404ab96ae4d0a954b113a31d3fb50"

app = Flask(__name__)

# Clarifai model
model = Model(
    user_id="clarifai",
    app_id="main",
    model_id="food-item-recognition",
    pat=PAT
)

# Load JSON
with open("nutrition.json") as f:
    nutrition_data = json.load(f)

@app.route('/')
def home():
    return render_template("index.html")

# 🔍 SEARCH FUNCTION
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('food')

    if not query:
        return render_template("index.html",
                               food="Not Found",
                               calories="-",
                               protein="-",
                               fat="-",
                               sugar="-")

    query = query.lower().strip()

    matched_food = None

    # 🔥 SMART MATCHING
    for key in nutrition_data:
        if query in key or key in query:
            matched_food = key
            break

    if not matched_food:
        return render_template("index.html",
                               food="Not Found",
                               calories="-",
                               protein="-",
                               fat="-",
                               sugar="-")

    result = nutrition_data[matched_food]

    return render_template("index.html",
                           food=matched_food,
                           calories=result["calories"],
                           protein=result["protein"],
                           fat=result["fat"],
                           sugar=result["sugar"])


# 📸 IMAGE ANALYSIS
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'image' not in request.files or request.files['image'].filename == "":
        return render_template("index.html",
                               food="Not Found",
                               calories="-",
                               protein="-",
                               fat="-",
                               sugar="-")

    image = request.files['image']
    image_bytes = image.read()

    prediction = model.predict_by_bytes(image_bytes)

    concept = prediction.outputs[0].data.concepts[0]
    food_name = concept.name.lower()
    confidence = concept.value

    # ❌ Low confidence
    if confidence < 0.8:
        return render_template("index.html",
                               food="Not Found",
                               calories="-",
                               protein="-",
                               fat="-",
                               sugar="-")

    matched_food = None

    # 🔥 SMART MATCHING
    for key in nutrition_data:
        if key in food_name or food_name in key:
            matched_food = key
            break

    if not matched_food:
        return render_template("index.html",
                               food="Not Found",
                               calories="-",
                               protein="-",
                               fat="-",
                               sugar="-")

    result = nutrition_data[matched_food]

    return render_template("index.html",
                           food=matched_food,
                           calories=result["calories"],
                           protein=result["protein"],
                           fat=result["fat"],
                           sugar=result["sugar"])


if __name__ == "__main__":
    app.run(debug=True)