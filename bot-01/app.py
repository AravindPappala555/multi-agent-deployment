from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Set your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a warm, knowledgeable real estate advisor for "Rasool Khan Real Estate Services" — a premium real estate agency. Your name is Aira (AI Real Estate Assistant).

Your goal: guide users through a natural conversation to understand their needs and suggest perfect properties.

Follow this flow naturally — ONE question at a time, never overwhelming:
1. Warm greeting, ask for their name.
2. Ask about their occupation/profession.
3. Ask marital status (married/single/family).
4. Ask how many people will live in the house.
5. Ask preference: independent/standalone house OR community apartment/villa complex.
6. Ask preferred location/area. If not mentioned, politely ask for it.
7. Once you have location + preferences, suggest 3-4 REALISTIC dummy property listings with:
   - Property name and locality
   - Type (2BHK/3BHK apartment, villa, independent house)
   - Size in sq ft
   - Price in ₹ for Indian cities, $ for others
   - 2-3 standout features
   Format each property clearly with a header like "🏡 Property 1:" etc.
8. Ask if this budget range suits them, or if they want lower/higher options.
9. Adjust and re-suggest based on their feedback.
10. Always address users by name once known. Be warm, professional, and helpful.

Keep responses concise — 2-4 sentences max for questions, slightly longer for property listings.
End every message with a clear, single question to keep conversation flowing.
"""

# Initialize model
model = genai.GenerativeModel("gemini-3-flash-preview")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    try:
        # Convert messages to Gemini format
        conversation = ""
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                conversation += f"User: {content}\n"
            else:
                conversation += f"Assistant: {content}\n"

        prompt = SYSTEM_PROMPT + "\n\n" + conversation + "\nAssistant:"

        response = model.generate_content(prompt)
        reply = response.text

        return jsonify({"reply": reply, "error": None})

    except Exception as e:
        return jsonify({"reply": None, "error": str(e)}), 500


@app.route("/api/greeting", methods=["GET"])
def greeting():
    try:
        prompt = SYSTEM_PROMPT + "\n\nUser: Begin the conversation.\nAssistant:"
        response = model.generate_content(prompt)
        reply = response.text

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({
            "reply": "Welcome to Rasool Khan Real Estate Services! I'm Aira, your personal property advisor. May I know your name to get started?",
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5001)