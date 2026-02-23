import json
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "admissions.json")

def save_admission(data):
    data["time"] = datetime.now().isoformat()

    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

    with open(DB_FILE, "r+") as f:
        records = json.load(f)
        records.append(data)
        f.seek(0)
        json.dump(records, f, indent=2)