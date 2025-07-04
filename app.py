from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import re, string, requests

app = Flask(__name__)

# Load model/vectorizer
model = joblib.load("lr_model.jb")
vectorizer = joblib.load("vectorizer.jb")

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)       # Remove URLs
    text = re.sub(r"\d+", "", text)           # Remove digits
    text = re.sub(r"[^\w\s]", "", text)       # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
    return text


# Fetch latest news via NewsAPI
NEWS_API_KEY = "b5263232c0ab4d71b2f909ff36259045"

def get_latest_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=1&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        articles = res.json().get("articles", [])
        if articles:
            article = articles[0]
            return article["title"] + " " + (article.get("description") or "")
    except Exception as e:
        print("❌ NewsAPI Error:", e)
    return ""

# Home Route
@app.route('/')
def home():
    latest_news = get_latest_news()
    try:
        df = pd.read_csv("news_dataset_small.csv").dropna()
        samples = df[['title', 'text']].sample(8).to_dict(orient='records')
    except:
        samples = []
    return render_template("index.html", latest_news=latest_news, samples=samples)

# Prediction API
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No news text provided"}), 400

    cleaned = clean_text(data['text'])
    vect = vectorizer.transform([cleaned])
    prediction = model.predict(vect)[0]
    proba = model.predict_proba(vect)[0]
    confidence = round(proba[prediction] * 100, 2)

    result = "Uncertain"
    if confidence >= 60:
        result = "Fake News" if prediction == 1 else "Real News"

    return jsonify({"result": result, "confidence": confidence})


@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Optional: Save to CSV or print to console
    print("Name:", name)
    print("Email:", email)
    print("Subject:", subject)
    print("Message:", message)

    # Show thank you page with user's name
    return render_template('thankyou.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
