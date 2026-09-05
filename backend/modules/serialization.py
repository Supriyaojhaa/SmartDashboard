import json
import os
import tempfile

IS_VERCEL = os.environ.get("VERCEL") == "1"

if IS_VERCEL:
    DATA_DIR = os.path.join(tempfile.gettempdir(), "data")
else:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

DATA_FILE = os.path.join(DATA_DIR, "datasets.json")

def save_results(stats):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)

        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        else:
            data = {}

        data["latest_run"] = stats

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Warning writing serialization data: {e}")