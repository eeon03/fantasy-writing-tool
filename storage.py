import json
import os

def save(filename, data):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

def load(filename):
    filepath = f"data/{filename}.json"
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)
