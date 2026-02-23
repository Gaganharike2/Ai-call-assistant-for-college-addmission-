from flask import Blueprint, render_template, request

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def home():
    return render_template("index.html")

@pages_bp.route("/courses")
def courses():
    return render_template("courses.html")

@pages_bp.route("/fees")
def fees():
    return render_template("fees.html")

@pages_bp.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@pages_bp.route("/admission-process")
def admission_process():
    return render_template("admission-process.html")

@pages_bp.route("/admission")
def admission_page():
    course = request.args.get("course")
    return render_template("admission.html", course=course)