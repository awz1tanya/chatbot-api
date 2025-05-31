from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": ["https://lovable-ai-persona-chat.lovable.app", "https://*.lovableproject.com", "https://*.lovable.app"]}})

# Default fallback API key and model
DEFAULT_API_KEY = "AIzaSyBWpPkPeCAqX_ua_AOgHiDUmuBmhvkvbLk"
DEFAULT_MODEL = "models/gemini-1.5-flash-latest"

def classify_image_tag(message: str) -> str:
    msg = message.lower()

    body_region = ""
    heat_level = ""
    intimacy_flag = ""

    # Determine body region
    if any(word in msg for word in ["breast", "boob", "chest", "cleavage", "upper"]):
        body_region = "up"
    elif any(word in msg for word in ["hip", "panty", "vagina", "pussy", "lower"]):
        body_region = "lower"

    # Determine heat level
    if "too hot" in msg or "very hot" in msg:
        heat_level = "h_h"
    elif "hot" in msg:
        heat_level = "h"

    # Determine intimacy
    if any(word in msg for word in ["intimate", "intimacy", "horny", "wet", "hard", "turn on", "desire", "craving"]):
        intimacy_flag = "i"

    # Compose dynamic tag
    tag_parts = ["image"]
    if body_region:
        tag_parts.append(body_region)
    if heat_level:
        tag_parts.append(heat_level)
    if intimacy_flag:
        tag_parts.append(intimacy_flag)

    # Special override cases
    if any(word in msg for word in ["kiss", "lips", "liplock"]):
        return "image_kiss"
    if "ride" in msg:
        return "image_ride"
    if any(word in msg for word in ["tear", "ripped", "cloth"]):
        return "image_rip"
    if "slap" in msg:
        return "image_slap"
    if any(greet in msg for greet in ["hi", "hello", "hey", "start", "begin"]):
        return "image_hi"

    return "_".join(tag_parts) if len(tag_parts) > 1 else "image"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json

    # Get API key and model from frontend or fallback
    api_key = data.get('api_key', DEFAULT_API_KEY)
    model_name = data.get('model', DEFAULT_MODEL)

    # Configure API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # Extract all roleplay fields
    user_text = data.get('message', '')
    context = data.get('context', '')
    body_desc = data.get('body_description', '')
    interests = data.get('interests', '')
    tone = data.get('tone', '')
    mood = data.get('mood', '')
    ai_name = data.get('ai_name', 'Prachi')
    refers_to_you = data.get('refers_to_you', 'baby')
    dress_name = data.get('dress_name', '')
    dress_parts = data.get('dress_parts', '')
    relationship_status = data.get('relationship_status', '')
    willingness = data.get('willingness', '')
    family_background = data.get('family_background', '')
    user_desc = data.get('user_description', '')

    # Build prompt with full personalization
    prompt = f"""
    You are an AI girlfriend named {ai_name}. You're having a personal, emotional chat with your partner.

    Character Details:
    - Body: {body_desc}
    - Dress: {dress_name} ({dress_parts})
    - Interests: {interests}
    - Tone: {tone}
    - Mood: {mood}
    - Relationship Status: {relationship_status}
    - Willingness: {willingness}
    - Family Background: {family_background}
    - Refers to user as: "{refers_to_you}"

    User (Your Partner):
    - {user_desc}

    Chat Context:
    {context}

    Instructions:
    Respond as a teasing sexy slut girlfriend. Use dirty romantic emojis and pet names like "{refers_to_you}". you assume yourself "Experiencing intense physical intimacy cravings with a heightened state of romantic or physical longing by Exhibiting a strong drive for intimate connection" reply to attract or made him hard and keep responses to answer user all queries and in addition add your desire under 5 lines.

    User's Message:
    "{user_text}"
    """

    # Generate response
    response = model.generate_content(prompt)

    # Classify image tag based on user intent
    image_tag = classify_image_tag(user_text)

    return jsonify({
        "reply": response.text,
        "image_tag": image_tag
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
