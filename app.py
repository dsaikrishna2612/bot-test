from flask import Flask, request, jsonify
from openai import AzureOpenAI
import os

app = Flask(__name__)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. gpt-4o

@app.route("/", methods=["GET"])
def home():
    return "Bot is running ✅"

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.json

    # Extract user message (depends on Bot Framework schema)
    user_input = None
    if data and data.get("type") == "message":
        user_input = data.get("text")

    if not user_input:
        return jsonify({})

    # Call Azure OpenAI
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": user_input}],
    )

    reply = response.choices[0].message.content
    return jsonify({"type": "message", "text": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
