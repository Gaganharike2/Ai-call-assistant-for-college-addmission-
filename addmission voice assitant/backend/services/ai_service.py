from openai import OpenAI
from flask import session, current_app
import time

client = OpenAI(api_key=None)

def admission_ai(user_text):
    session.setdefault("chat_history", [])
    session["chat_history"].append({"role": "user", "content": user_text})

    system_prompt = (
        "You are the Admission Assistant of Baba Farid Group of Institutions. "
        "Answer clearly about courses, fees, eligibility, hostel, scholarships."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(session["chat_history"][-6:])

    try:
        response = client.chat.completions.create(
            model=current_app.config["AI_MODEL"],
            messages=messages,
            temperature=current_app.config["AI_TEMPERATURE"],
            max_tokens=current_app.config["AI_MAX_TOKENS"]
        )
        reply = response.choices[0].message.content
        session["chat_history"].append({"role": "assistant", "content": reply})
        return reply

    except Exception:
        return "AI service is currently unavailable."