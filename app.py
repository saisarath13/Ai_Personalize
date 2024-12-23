from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
import boto3
import torch

app = Flask(__name__)

# Globals for lazy loading
model = None
tokenizer = None

def load_model():
    global model, tokenizer

    # S3 bucket details
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    model_key = os.environ.get("MODEL_KEY")
    tokenizer_files_prefix = os.environ.get("TOKENIZER_KEY_PREFIX")

    if not bucket_name or not model_key or not tokenizer_files_prefix:
        raise ValueError("Environment variables S3_BUCKET_NAME, MODEL_KEY, and TOKENIZER_KEY_PREFIX must be set.")

    # Paths for downloaded files
    model_path = "/tmp/model.safetensors"
    tokenizer_dir = "/tmp/tokenizer"

    # Create directory for tokenizer
    os.makedirs(tokenizer_dir, exist_ok=True)

    # Download the model from S3
    s3 = boto3.client("s3")
    print("Downloading model from S3...")
    s3.download_file(bucket_name, model_key, model_path)

    # Download tokenizer files
    tokenizer_files = ["config.json", "vocab.json", "merges.txt", "tokenizer_config.json", "generation_config.json"]
    for file_name in tokenizer_files:
        s3.download_file(bucket_name, f"{tokenizer_files_prefix}/{file_name}", f"{tokenizer_dir}/{file_name}")

    # Load model and tokenizer
    print("Loading model and tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_dir)
    model = GPT2LMHeadModel.from_pretrained(tokenizer_dir, torch_dtype=torch.float32)
    model.load_state_dict(torch.load(model_path))
    print("Model and tokenizer loaded successfully.")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    global model, tokenizer
    if model is None or tokenizer is None:
        load_model()

    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    response = generate_response(question)
    return jsonify({"response": response})

def generate_response(question):
    if not question.endswith("?"):
        question += "?"

    input_text = f"Question: {question} Answer briefly:"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=50, truncation=True)
    output = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=70,
        no_repeat_ngram_size=3,
        repetition_penalty=2.0,
        temperature=0.7,
        top_p=0.9,
        num_beams=5,
        early_stopping=True,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.split(".")[0].strip() + "."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
