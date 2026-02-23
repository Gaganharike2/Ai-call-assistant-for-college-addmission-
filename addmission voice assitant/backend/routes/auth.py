from flask import Blueprint, request, jsonify, session
from utils.auth import verify_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if verify_user(username, password):
        session["user"] = username
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@auth_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})
