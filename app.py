from flask import Flask, request, jsonify
from openai import AzureOpenAI
import os, requests

app = Flask(__name__)

# Azure OpenAI credentials
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. gpt-4o

# Example tool: weather API
def get_weather(city: str):
    # Mock API response (replace with real API)
    return f"The weather in {city} is sunny 25°C."

tools = [
    {
        "name": "get_weather",
        "description": "Get weather info for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }
]

@app.route("/api/messages", methods=["POST"])
def messages():
    user_input = request.json.get("text")

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    msg = response.choices[0].message

    # If tool call requested
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            if tool_call.function.name == "get_weather":
                city = tool_call.function.arguments.get("city")
                weather = get_weather(city)
                return jsonify({"reply": weather})

    return jsonify({"reply": msg.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
