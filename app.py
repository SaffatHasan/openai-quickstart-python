import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# TODO: Cache this in a file instead.
def get_models():
    response = openai.Model.list()
    data = response["data"]
    return [model['id'] for model in data]

# Load models at the start as a global variable so we don't keep
# asking.
AVAILABLE_MODELS = get_models()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", model_choices=AVAILABLE_MODELS)

@app.route("/prompt", methods=["POST"])
def prompt():
    prompt = request.form["prompt"]
    model = request.form["model"]
    if model not in AVAILABLE_MODELS:
        new_line = '\n'
        return f"ERROR: {model} is not a valid model. Must be one of:\n{new_line.join(AVAILABLE_MODELS)}"
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
    )
    print(f"DEBUG: {response=}")
    return response.choices[0].text

