import json
import os

DATA_FILE = "data/datasets.json"

def save_results(stats):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data["latest_run"] = stats

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)