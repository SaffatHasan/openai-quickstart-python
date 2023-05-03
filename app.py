import os

import openai
from flask import Flask, render_template, request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# https://platform.openai.com/docs/models/model-endpoint-compatibility
COMPLETION_MODELS = [
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]

# CHAT_MODELS = [
#     "gpt-4",
#     "gpt-4-0314",
#     "gpt-4-32k",
#     "gpt-4-32k-0314",
#     "gpt-3.5-turbo",
#     "gpt-3.5-turbo-0301",
# ]

AVAILABLE_MODELS = sorted(COMPLETION_MODELS)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", model_choices=AVAILABLE_MODELS)

@app.route("/prompt", methods=["POST"])
def prompt():
    if request.form.get("dry_run"):
        return "\n\nWagging tails, so happy\nLoyal friends, our joys"

    prompt = request.form["prompt"]
    model = request.form["model"]
    if model not in AVAILABLE_MODELS:
        new_line = '\n'
        return f"ERROR: {model} is not a valid model. Must be one of:\n{new_line.join(AVAILABLE_MODELS)}"

    # TODO: add support for more than text completion.
    # https://github.com/openai/openai-python#chat
    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=0.5,
        )
    except openai.error.InvalidRequestError as e:
        return str(e)

    print(f"DEBUG: {response=}")
    return response.choices[0].text
