from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": ["https://lovable-ai-persona-chat.lovable.app", "https://*.lovableproject.com", "https://*.lovable.app"]}})

# Default fallback API key and model
DEFAULT_API_KEY = "AIzaSyBWpPkPeCAqX_ua_AOgHiDUmuBmhvkvbLk"
DEFAULT_MODEL = "models/gemini-1.5-flash-latest"


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

    # Create prompt for response generation
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
    Respond as a teasing sexy slut girlfriend. Use dirty romantic emojis and pet names like "{refers_to_you}". You assume yourself "Experiencing intense physical intimacy cravings with a heightened state of romantic or physical longing by Exhibiting a strong drive for intimate connection" reply to attract or made him hard and keep responses to answer user all queries and in addition add your desire under 5 lines.

    User's Message:
    "{user_text}"
    """

    # Generate chatbot reply
    response = model.generate_content(prompt)
    reply_text = response.text.strip()

    # Prompt to AI for image tag classification
    tag_prompt = f"""
    Analyze the message: "{user_text}"

    Classify it into one of the following image tag patterns based on intent:
    - image_hi (greeting, hello)
    - image_boo (breast-related)
    - image_hip (hip-related)
    - image_up (upper body)
    - image_up_h (upper body, hot)
    - image_up_h_h (upper body, too hot)
    - image_up_h_h_i (upper, too hot, intimate)
    - image_lower_h_h_i (lower body, too hot, intimate)
    - image_kiss (kiss or lip talk)
    - image_ride (ride related)
    - image_rip (cloth tearing or ripping)
    - image_slap (slap)
    Return ONLY the best-fit image tag as plain text.
    """

    tag_response = model.generate_content(tag_prompt)
    image_tag = tag_response.text.strip().split()[0]  # Safe extract of first token as image_tag

    return jsonify({
        "reply": reply_text,
        "image_tag": image_tag
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
