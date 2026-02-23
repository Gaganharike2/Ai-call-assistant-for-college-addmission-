import os
import json
import requests
from datetime import datetime

from flask import (
    Flask,
    request,
    jsonify,
    session,
    render_template,
    redirect,
    url_for,
    abort
)

from flask_cors import CORS
import bcrypt


# ==================================================
# PATH SETUP
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(BASE_DIR, "users.json")
COLLEGE_FILE = os.path.join(DATA_DIR, "college_info.txt")


# ==================================================
# FLASK APP
# ==================================================

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

app.secret_key = "college-admission-secret-key"

CORS(app)


# ==================================================
# LOGGING
# ==================================================

def log_event(event, data):

    record = {
        "time": datetime.now().isoformat(),
        "event": event,
        "data": data
    }

    with open(os.path.join(LOG_DIR, "activity.log"), "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


# ==================================================
# USER SYSTEM
# ==================================================

def save_users(users):

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def load_users():

    # Create admin if missing
    if not os.path.exists(USERS_FILE):

        pwd = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()

        users = [{
            "name": "Administrator",
            "username": "admin",
            "email": "admin@bfgi.com",
            "mobile": "9999999999",
            "password": pwd,
            "role": "Admin"
        }]

        save_users(users)

        return users


    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)


    # Auto-fix users
    updated = False

    for u in users:

        if "name" not in u:
            u["name"] = "User"
            updated = True

        if "email" not in u:
            u["email"] = "Not Set"
            updated = True

        if "mobile" not in u:
            u["mobile"] = "Not Set"
            updated = True

        if "role" not in u:
            u["role"] = "Student"
            updated = True


    if updated:
        save_users(users)


    return users


# ==================================================
# AUTH HELPERS
# ==================================================

def login_required():
    return "user" in session


def admin_required():

    return "user" in session and session.get("role") == "Admin"


def get_current_user():

    username = session.get("user")

    if not username:
        return None


    users = load_users()

    for u in users:
        if u["username"] == username:
            return u

    return None


# ==================================================
# COLLEGE DATA
# ==================================================

def load_college_data():

    if not os.path.exists(COLLEGE_FILE):

        default_data = """
Baba Farid Group of Institutions (BFGI)

Courses:
- BCA
- MCA
- B.Tech
- MBA
- BBA
- B.Com

Fees:
BCA: 45000
MCA: 60000
B.Tech: 80000
MBA: 70000

Location:
Bathinda, Punjab

Contact:
info@bfgi.com
"""

        with open(COLLEGE_FILE, "w", encoding="utf-8") as f:
            f.write(default_data)


    with open(COLLEGE_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ==================================================
# AI SYSTEM
# ==================================================

def admission_ai(user_text):

    try:

        college_data = load_college_data()


        prompt = f"""
You are BFGI Admission Assistant.

Use ONLY given data.

DATA:
{college_data}

Question:
{user_text}

Answer:
"""


        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )


        if r.status_code != 200:
            return "AI Service Error"


        data = r.json()

        return data.get("response", "No reply")


    except Exception as e:

        print("OLLAMA ERROR:", e)

        return "AI Offline"


# ==================================================
# AUTH PAGES
# ==================================================

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


# ==================================================
# LOGIN API
# ==================================================

@app.route("/api/login", methods=["POST"])
def login_api():

    data = request.get_json()

    users = load_users()


    for u in users:

        if u["username"] == data.get("username"):

            if bcrypt.checkpw(
                data.get("password", "").encode(),
                u["password"].encode()
            ):

                session["user"] = u["username"]
                session["role"] = u["role"]

                log_event("login", u["username"])
                return jsonify({
                    "status": "success",
                    "role": u["role"]
                })


    return jsonify({"status": "error"}), 401


# ==================================================
# REGISTER API
# ==================================================

@app.route("/api/register", methods=["POST"])
def register_api():

    data = request.get_json()

    users = load_users()


    for u in users:
        if u["username"] == data["username"]:
            return jsonify({"status": "error"})


    pwd = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    ).decode()


    user = {
        "name": data["name"],
        "username": data["username"],
        "email": data["email"],
        "mobile": data["mobile"],
        "password": pwd,
        "role": "Student"
    }


    users.append(user)

    save_users(users)

    log_event("register", data["username"])

    return jsonify({"status": "success"})


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login_page"))


# ==================================================
# FRONTEND PAGES
# ==================================================

@app.route("/")
def home():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("index.html")


# ✅ FIXED RECOMMEND ROUTE
@app.route("/recommend")
def recommend():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("recommend.html")


@app.route("/chatbot")
def chatbot():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("chatbot.html")


@app.route("/courses")
def courses():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("courses.html")


@app.route("/fees")
def fees():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("fees.html")


@app.route("/admission-process")
def admission_process():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("admission-process.html")


@app.route("/admission")
def admission():

    if not login_required():
        return redirect(url_for("login_page"))

    return render_template("admission.html")


# ==================================================
# PROFILE
# ==================================================

@app.route("/profile")
def profile():

    if not login_required():
        return redirect(url_for("login_page"))


    user = get_current_user()

    if not user:
        return redirect(url_for("logout"))


    return render_template("profile.html", user=user)


# ==================================================
# ADMIN PANEL
# ==================================================

@app.route("/admin")
def admin_panel():

    if not admin_required():
        abort(403)


    users = load_users()


    stats = {
        "total_users": len(users),
        "students": len([u for u in users if u["role"] == "Student"]),
        "admins": len([u for u in users if u["role"] == "Admin"])
    }


    return render_template(
        "admin.html",
        users=users,
        stats=stats
    )


# ==================================================
# ADMIN APIs
# ==================================================

@app.route("/api/admin/users")
def admin_users():

    if not admin_required():
        return jsonify({"error": "Forbidden"}), 403


    return jsonify(load_users())


@app.route("/api/admin/delete/<username>")
def admin_delete_user(username):

    if not admin_required():
        return jsonify({"error": "Forbidden"}), 403


    users = load_users()

    users = [u for u in users if u["username"] != username]

    save_users(users)

    log_event("delete_user", username)

    return jsonify({"status": "success"})


# ==================================================
# CHAT API
# ==================================================

@app.route("/api/chat", methods=["POST"])
def chat_api():

    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401


    data = request.get_json()

    reply = admission_ai(data.get("message", ""))

    return jsonify({"reply": reply})


# ==================================================
# APPLY API
# ==================================================

@app.route("/api/apply", methods=["POST"])
def apply_admission():

    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401


    data = request.get_json()

    log_event("apply", data)

    return jsonify({"status": "success"})


# ==================================================
# HEALTH
# ==================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "running",
        "time": datetime.now().isoformat()
    })


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
