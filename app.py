from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import re
import string

app = Flask(__name__)

#  Load model and vectorizer at the top
model = joblib.load("lr_model.jb")
vectorizer = joblib.load("vectorizer.jb")

#  Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

#  Home page route
@app.route('/')
def home():
    df = pd.read_csv("news_dataset_small.csv").dropna()
    samples = df[['title', 'text']].sample(8).to_dict(orient='records')
    return render_template("index.html", samples=samples)

import csv
from flask import request, render_template

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.form.to_dict()

        # Debug print (optional)
        print("📥 Received form data:", data)

        # Save to CSV
        with open('messages.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([data.get('name'), data.get('email'), data.get('subject'), data.get('message')])

        # Render thank you page
        return render_template('thankyou.html', name=data['name'])

    except Exception as e:
        print("❌ Error saving form data:", e)
        return "Something went wrong. Please try again."


# API prediction route
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No news text provided"}), 400

    cleaned = clean_text(data['text'])
    vect = vectorizer.transform([cleaned])
    prediction = model.predict(vect)[0]

    return jsonify({"result": "Fake News" if prediction == 1 else "Real News"})

if __name__ == "__main__":
    app.run()
