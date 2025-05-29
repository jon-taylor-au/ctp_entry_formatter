import os
import json
from src.webapp_class import APIClient
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
BASE_URL = os.getenv("BASE_URL")  
LOGIN_PAGE_URL = f"{BASE_URL}/authed/user.action?cmd=welcome"
LOGIN_URL = f"{BASE_URL}/authed/j_security_check"
JSON_FILE = "outputs/json_exports/chronology_writeback.json"
EXCLUDED_IDS = []  # Add IDs to exclude if needed

# --- Load and optionally filter data ---
def load_cleaned_payload(path, exclude_ids=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if exclude_ids:
            before = len(data)
            data = [entry for entry in data if str(entry.get("id")) not in exclude_ids]
            print(f"Excluded {before - len(data)} entries based on ID filter")
        return data
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return []

# --- Upload payload ---
def upload_chronology(client, court_book_id, payload):
    url = f"/api/v0/books/{court_book_id}/chronology/"
    response = client.send_put_request(url, payload)
    if response and response.status_code == 200:
        print(f"Successfully updated Court Book ID {court_book_id} to {BASE_URL}.")
    else:
        print(f"Failed to update Court Book ID {court_book_id}. Status: {response.status_code if response else 'N/A'}")

# --- Main execution ---
def main():
    court_book_id = os.getenv("BOOK_ID")
    if not court_book_id:
        print("BOOK_ID environment variable not found.")
        return

    client = APIClient(BASE_URL, LOGIN_PAGE_URL, LOGIN_URL)
    if not client.authenticate():
        print("Authentication failed.")
        return

    payload = load_cleaned_payload(JSON_FILE, exclude_ids=EXCLUDED_IDS)
    if not payload:
        print("No data to upload.")
        return

    # 🔁 Automatically upload without confirmation
    print(f"Uploading cleaned chronology to Court Book ID {court_book_id}...")
    upload_chronology(client, court_book_id, payload)

if __name__ == "__main__":
    main()
