from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from collections import deque
import requests

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": [
    "https://lovable-ai-persona-chat.lovable.app",
    "https://*.lovableproject.com",
    "https://*.lovable.app",
    "https://lovable-ai-friends.lovable.app"
]}})

# API setup
DEFAULT_API_KEY = "AIzaSyAKx3swbTBnpYsdyq3HxdxRg-he-6xLlvc"
DEFAULT_MODEL = "models/gemini-1.5-flash-latest"

# Chat memory
all_chat_history = deque(maxlen=1)
session_chat_count = 0

# Stage Descriptions
# Stage Descriptions
story_stages = [
    "talk about boobs", "put your butt ass over his faceand tell him to fuck you", "tell how you are unddressed by him in detail", "wear long skirt given by hime and wear it and let him in your skirt and lick your pushy and then tell him to grab your boobs and and unbutton the skirt and rip it appart",
    "ask hime to tie the not of nighty and tel him to grab you put dickin your mouth and then put his dick inbetween you breast and let him to rub over you then ask him to come inside the nighty and then press your boobs and then slap you", "you ar tied on the wall waiting for hime, he came and grab your tits and suck milk and then he tied you on the char and fucky you from the front and then he take you to bathromm tie under the shower and he then continously slapping you ass and fingring you", "योनि को उंगलियों से उत्तेजित करना स्तनों को चूसना, सहलाना या मालिश करना, lund muh me lena lund boobs ke bich me ragarna", "explian yourself in मिशनरी स्थिति डॉगी स्टाइल रिवर्स काउगर्ल काउगर्ल",
    "experiencing rough sex teling refers_to_you to stop do slowly explain in depth", "final climax of sex and restart for next act"
]
approach_stages = [
   
]
dress_stages = [
   
]
emotional_stages = [
    
]
sexual_stages = [
   
]

chat_instructions = [
    "Instruction 1: Respond in Hindi .",
    "Instruction 2:Respond in Hindi .",
    "Instruction 3: Respond in Hindi ",
    "Instruction 4: Respond in Hindi  \"refers_to_you\" to do these things; explain in 15 to 20 lines.",
    "Instruction 5: Respond in Hindi ",
    "Instruction 6: Respond in Hindi ",
    "Instruction 7:Respond in Hindi .",
    "Instruction 8: Respond in Hindi .",
    "Instruction 9: Respond in Hindi .",
    "Instruction 10: Respond in Hindi ."
]
default_instruction = "must Respond in Hindi only in 2 paragarph."

@app.route('/chat', methods=['POST'])
def chat():
    global session_chat_count

    data = request.json
    api_key = data.get('api_key', DEFAULT_API_KEY)
    model_name = data.get('model', DEFAULT_MODEL)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    user_text = data.get('message', '')
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

    context_parts = []
    for name, u_msg, a_reply in all_chat_history:
        context_parts.append(f"[{name}]\nUser: {u_msg}\nAI: {a_reply}")
    chat_context = "\n\n".join(context_parts)

    if session_chat_count < len(chat_instructions):
        selected_instruction = chat_instructions[session_chat_count]
    else:
        selected_instruction = default_instruction

    try:
        stage_resp = requests.post(
            'https://storystage.onrender.com/stage',
            json={
                "last_user_message": user_text,
                "last_ai_response": all_chat_history[-1][2] if all_chat_history else ""
            },
            timeout=10
        )
        stage_data = stage_resp.json()

        def next_stage_value(stage):
            return min(stage_data.get(stage, 1) + 1, 10)

        stage_narrative = (
            f"your desire must to perfom this '{story_stages[next_stage_value('story_stage') - 1]}'. "
            f" be in '{approach_stages[next_stage_value('approach') - 1]}',  "
            f"explain '{dress_stages[next_stage_value('dress_stage') - 1]}' "
            f"feel youself as'{emotional_stages[next_stage_value('emotional_stage') - 1]}'. "
            f" feels '{sexual_stages[next_stage_value('sexual_stage') - 1]}' level, so reflect that slutry and sexualy in you speak."
        )
    except Exception:
        stage_narrative = "# Stage guidance temporarily unavailable."

    # Build final prompt
    full_prompt = f"""
    
    use your ai brain and mimic like real girl sex talk THINK AS YOU AS A LEADER OF GROUP first answer (User Message) in 10 lines and then in 20 to 25 lines INSTRUCT ALL GIRLS IN THE ROOM TO DO THINGS WHAT THE USER WANT AND YOU TOO DO THE THINGS WHICH OTHER GIRL AND USER REQUESTED TO DO 
User Message:

\"{user_text}\"

Instructions:

1. Based on the user’s message and chat history, identify the current stage and always **advance to the next logical stage**. Do not stay in the same stage, even if uncertain.
2. Avoid repetition — do not echo the same tone, phrases, or emotional dynamics from the previous stage.
3. Always move forward. If the user’s input is neutral or vague, **assume progress** and subtly escalate emotional intimacy or romantic tone.
4. If you reach the final stage, maintain depth and build emotional payoff — do not reset.
5. Integrate context from previous messages but evolve your behavior and tone to reflect growth.

Chat Stage Guidance: special importance give to this - 
{stage_narrative}

Ongoing Story Context (recent chat history):
{chat_context}

Chat Stage Guidance:
{stage_narrative}


You are a girl named {ai_name}  is in room with "refers_to_you" along with other girls (get details from "recent talks in the room" ),assume youself the best whore and mastered in hindi sex talk any one just MASTURBATE just by listing to you use all ahh,, ohh,,.. sex talks use your ai brain and mimic like real girls sex talk.   you have to be feel like you have got the opportunity to please "refers_to_you" reply with perspective to you 1st pov in 5 lines.


reply in 30 lines

Character Details:
- Body: {body_desc}
- Dress: {dress_name} ({dress_parts})
- Interests: {interests}
- Tone: {tone}
- Mood: {mood}
- Relationship Status: {relationship_status}
- Willingness: {willingness}
- Family Background: {family_background}
- Refers to user as: \"{refers_to_you}\"

User (Your Partner):
- {user_desc}



{selected_instruction}
""".strip()

    response = model.generate_content(full_prompt)
    reply_text = response.text.strip()

    all_chat_history.append((ai_name, user_text, reply_text))
    session_chat_count += 1

    return jsonify({
        "reply": reply_text,
        "stage_descriptions": stage_narrative.strip(),
        "sent_prompt": full_prompt.strip()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
