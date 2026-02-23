import json
import os
import bcrypt

USERS_DB = os.path.join(
    os.path.dirname(__file__), "..", "database", "users.json"
)

def get_users():
    with open(USERS_DB, "r") as f:
        return json.load(f)

def verify_user(username, password):
    users = get_users()
    for user in users:
        if user["username"] == username:
            return bcrypt.checkpw(
                password.encode(),
                user["password"].encode()
            )
    return False
