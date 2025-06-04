# src/fetch_api_data.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from src.webapp_class import APIClient

# --- Load environment variables ---
load_dotenv()

# --- Configuration ---
BASE_URL = os.getenv("BASE_URL")
OUTPUT_FOLDER = Path("outputs/json_exports")

BOOK_ID = os.environ.get("BOOK_ID")
if not BOOK_ID:
    raise ValueError("BOOK_ID environment variable not set")

#BOOK_ID = 11452

if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")
if not BOOK_ID:
    raise ValueError("BOOK_ID environment variable not set")

LOGIN_PAGE = f"{BASE_URL}/authed/user.action?cmd=welcome"
LOGIN_URL = f"{BASE_URL}/authed/j_security_check"

# --- Ensure output folder exists ---
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def save_json(data, name):
    path = OUTPUT_FOLDER / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {path}")

def fetch_data():
    client = APIClient(BASE_URL, LOGIN_PAGE, LOGIN_URL)

    if not client.authenticate():
        raise RuntimeError("Authentication failed")

    print(f"Fetching data for book ID: {BOOK_ID}")

    endpoints = {
        "chronology_raw": f"/api/v0/books/{BOOK_ID}/chronology/",
        "bookitems": f"/api/v0/books/{BOOK_ID}/chronology/bookitems/"
    }

    for name, endpoint in endpoints.items():
        data = client.fetch_api_data(endpoint)
        if data:
            save_json(data, name)

def enrich_chronology():
    chrono_path = OUTPUT_FOLDER / "chronology_raw.json"
    items_path = OUTPUT_FOLDER / "bookitems.json"
    output_path = OUTPUT_FOLDER / "chronology.json"

    with open(chrono_path, "r", encoding="utf-8") as f:
        chronology = json.load(f)

    with open(items_path, "r", encoding="utf-8") as f:
        book_items = json.load(f)

    lookup = {item["id"]: item for item in book_items}

    for entry in chronology:
        match = lookup.get(entry.get("bookItemId"))
        if match:
            entry["description"] = match.get("description")
            entry["documentType"] = match.get("documentType")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chronology, f, ensure_ascii=False, indent=2)

    print(f"Enriched chronology saved to: {output_path}")

def main():
    fetch_data()
    enrich_chronology()

if __name__ == "__main__":
    main()
