# src/fetch_api_data.py

import os
import json
import sys
from src.webapp_class import APIClient
from dotenv import load_dotenv
load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL")
LOGIN_PAGE = f"{BASE_URL}/authed/user.action?cmd=welcome"
LOGIN_URL = f"{BASE_URL}/authed/j_security_check"
OUTPUT_FOLDER = "outputs/json_exports"

BOOK_ID = os.environ.get("BOOK_ID")
if not BOOK_ID:
    raise ValueError("BOOK_ID environment variable not set")

#BOOK_ID = 11410

print(f"Using BOOK_ID: {BOOK_ID}")

if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")


# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def save_json(data, endpoint_name):
    filename = f"{endpoint_name}.json"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filepath}")

def main():
    client = APIClient(BASE_URL, LOGIN_PAGE, LOGIN_URL)

    if not client.authenticate():
        print("Authentication failed.")
        return

    print(f"Fetching data for book ID: {BOOK_ID} from {BASE_URL}")

    endpoints = {
        #"book": f"/api/v0/books/{BOOK_ID}/",
        "chronology": f"/api/v0/books/{BOOK_ID}/chronology/"
        #"bookitems": f"/api/v0/books/{BOOK_ID}/chronology/bookitems/"
    }

    for name, endpoint in endpoints.items():
        data = client.fetch_api_data(endpoint)
        if data is not None:
            save_json(data, name)

if __name__ == "__main__":
    main()
