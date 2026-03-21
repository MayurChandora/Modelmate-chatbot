import os
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# Retrieve API key securely from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)

# Load knowledge file
with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if user_message.lower() in ["hi", "hello", "hey"]:
        return jsonify({"reply": "Hello!I am Modelmate :Machine Learning Model Selection ASSISTANT! How can i help you?"})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict assistant. You must answer the user's question based strictly and only on the provided Knowledge Base. "
                    "If the Knowledge Base does not contain a direct, complete answer to the user's question, you must reply exactly with: "
                    "'This information is not available in my knowledge base.' "
                    "Do not attempt to synthesize an answer from passing mentions of a word. Do not explain your reasoning. "
                    "Do not include any outside information."
                )
            },
            {
                "role": "user",
                "content": f"Knowledge Base:\n{knowledge}\n\nQuestion: {user_message}"
            }
        ],
        temperature=0.1
    )

    bot_reply = completion.choices[0].message.content
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)