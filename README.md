# 📚 Court Book Processing Automation

This solution automates the process of retrieving, cleaning, formatting, and archiving court book data using Python. It allows users to submit Book IDs via a shared Excel file, which is periodically read by a script that runs the full processing pipeline.

---

## 🗂 Folder Structure

```
project_root/
├── inputs/
│   └── book_id_queue.xlsx      # Shared Excel file where users enter Book IDs
├── outputs/                    # Holds output JSONs, HTML reports, etc.
├── processed/                  # Contains ZIP archives of processed outputs
├── src/
│   └── webapp_class.py         # API client class used for fetching data
├── 01_get_data.py              # Fetches raw data from API
├── 02_change_data.py           # Cleans and formats entryFinal HTML
├── 03_present_data.py          # Generates a visual comparison HTML report
├── 04_write_back.py            # (optional) Uploads the cleaned data back to the server
├── 05_cleanup.py               # Archives and deletes old output files
├── main.py                     # Main controller that loops through all Book IDs
└── README.md                   # This file
```

---

## How It Works

1. **User Input**: Users open `inputs/book_id_queue.xlsx` and enter Book IDs in the `BookID` column. They leave the `Status` column empty or set it to `Pending`.

2. **Scheduled Execution**: `main.py` is executed every 30 minutes (e.g. via Windows Task Scheduler).

3. **Queue Processing**:
    - Reads all rows where `Status` is not `Done`
    - For each `BookID`, the following scripts run in order:
      - `01_get_data.py`: Fetches data using the API
      - `02_change_data.py`: Cleans and structures HTML content
      - `03_present_data.py`: Generates an HTML report for review
      - `05_cleanup.py`: Archives output files and clears the working folder
    - Each script gets the current `BookID` via environment variable `BOOK_ID`

4. **Status Update**:
    - If all scripts succeed, the status is set to `Done`
    - If any script fails, the status is set to `Error`
    - A timestamp is written in the `Processed` column

---

## 📘 Excel File Format

Located at: `inputs/book_id_queue.xlsx`

| BookID | Status  | Processed           |
|--------|---------|---------------------|
| 11493  |         |                     |
| 11737  | Pending |                     |
| 11900  | Done    | 2025-05-26 14:45:33 |

> ✅ Only rows where Status ≠ "Done" will be processed.

---

## 🧠 Environment Variables

Each script uses the current Book ID via:
```
os.environ["BOOK_ID"]
```

No `.env` file is used. User credentials are entered at runtime for API access.

---

## 🛠 Prerequisites

- Python 3.10+
- Required packages: `pandas`, `openpyxl`, `requests`, `beautifulsoup4`

Install them with:
```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
pandas
openpyxl
requests
beautifulsoup4
```

---

##  Automation

Use Windows Task Scheduler to run `main.py` every X mins:

- Action: Start a program
- Program/script: `python`
- Arguments: `main.py`
- Start in: Full path to your project folder

---

## Best Practices

- Ensure Excel is **closed** before script runs (it cannot write to an open file).
- Users should only update the `BookID` and optionally set `Status` to `"Pending"`.
- Use version control (e.g. Git) to track changes to scripts.

---

##  Support

Contact your internal team or script maintainer for help configuring the scheduler or modifying script behavior.