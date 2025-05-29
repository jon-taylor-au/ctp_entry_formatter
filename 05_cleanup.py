import os
import zipfile
from pathlib import Path
import shutil
from datetime import datetime

# --- Configuration ---
SOURCE_DIR = Path("G:/01_Python/Projects/15_extraction_line_breaks/outputs")
TARGET_DIR = Path("G:/01_Python/Projects/15_extraction_line_breaks/processed")

# --- Get BOOK_ID from environment ---
book_id = os.environ.get("BOOK_ID", "unknown")

# --- Add timestamp suffix ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ZIP_FILE = TARGET_DIR / f"{book_id}_archived_files_{timestamp}.zip"

def zip_and_cleanup():
    if not SOURCE_DIR.exists():
        print(f"Folder not found: {SOURCE_DIR}")
        return

    print(f"Zipping contents of {SOURCE_DIR} to {ZIP_FILE.name}...")

    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in SOURCE_DIR.rglob("*"):
            if path.is_file():
                zipf.write(path, arcname=path.relative_to(SOURCE_DIR))

    print("Deleting all files and folders in source directory...")

    for item in SOURCE_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    print("Done.")

if __name__ == "__main__":
    zip_and_cleanup()
