from flask import Flask, request, jsonify
from Sentiment_Model import SentimentModel
import time

app = Flask(__name__)

path = './config/'

model = SentimentModel(
    vocap_pth = path + 'vocab-roberta-base.json',
    merges_pth = path + 'merges-roberta-base.txt',
    model_path = path
)

@app.route("/sentiment", methods=["POST"])
def predict():
    start_time = time.time()
    
    data = request.get_json()
    if "text" not in data:
        return jsonify({"error": "check text specifier format"})
    if "sentiment" not in data:
        return jsonify({"error": "check sentiment specifier format"})
    
    text = data["text"]
    sentiment = data["sentiment"]
    
    output = model.predict(input_text=text, sentiment=sentiment)
    
    duration = time.time() - start_time
    
    return jsonify({"prediction": output, "response time in seconds": duration})
    
    
if __name__ == "__main__":
    # (PowerSehll) Invoke-WebRequest -Uri http://127.0.0.1:5000/sentiment -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"text": "Hallo Simon!"}'
    app.run(host="0.0.0.0", port=5000)