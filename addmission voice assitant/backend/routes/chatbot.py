from flask import Blueprint, request, jsonify
from services.ai_service import admission_ai

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please type a message"})

    reply = admission_ai(message)
    return jsonify({"reply": reply})