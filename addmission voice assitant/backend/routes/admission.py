from flask import Blueprint, request, jsonify
from database.db import save_admission


admission_bp = Blueprint("admission", __name__, url_prefix="/api")

@admission_bp.route("/apply", methods=["POST"])
def apply():
    data = request.get_json()

    required = ["name", "email", "mobile", "course"]
    for field in required:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"{field} required"})

    save_admission(data)
    return jsonify({"status": "success", "message": "Application submitted"})