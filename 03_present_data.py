import json
from pathlib import Path
from jinja2 import Template

# --- Config ---
JSON_FILES = [
    "outputs/json_exports/chronology.json",
    #"outputs/json_exports/chronology_updated.json",
    "outputs/json_exports/chronology_writeback.json"
]
OUTPUT_HTML = "outputs/entry_comparison.html"

# --- Load Data ---
data_sets = []
for file_path in JSON_FILES:
    with open(file_path, "r", encoding="utf-8") as f:
        data_sets.append({entry["id"]: entry["entryFinal"] for entry in json.load(f)})

# --- Get All Unique Entry IDs ---
all_ids = sorted(set().union(*[set(d.keys()) for d in data_sets]))

# --- HTML Template ---
html_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EntryFinal Comparison</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th, td { border: 1px solid #ccc; padding: 10px; vertical-align: top; word-wrap: break-word; }
        th { background-color: #f5f5f5; }
        h2 { margin-top: 40px; }
    </style>
</head>
<body>
    <h1>Comparison of EntryFinal Values</h1>
    {% for entry_id in all_ids %}
        <h2>Entry ID: {{ entry_id }}</h2>
        <table>
            <tr>
                <th>Original</th>
                <th>Writeback</th>
            </tr>
            <tr>
                {% for dataset in data_sets %}
                    <td>{{ dataset.get(entry_id, "") | safe }}</td>
                {% endfor %}
            </tr>
        </table>
    {% endfor %}
</body>
</html>
""")

# --- Render and Save HTML ---
html_output = html_template.render(
    all_ids=all_ids,
    data_sets=data_sets
)

Path(OUTPUT_HTML).parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"HTML file generated: {OUTPUT_HTML}")
