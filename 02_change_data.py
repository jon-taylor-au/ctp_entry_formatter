import json
import re
from bs4 import BeautifulSoup
from pathlib import Path

# --- Config ---
INPUT_FILE = Path("outputs/json_exports/chronology.json")
OUTPUT_FILE = Path("outputs/json_exports/chronology_writeback.json")

# Exclusion filters — match any of these to skip an entry
EXCLUDE_TYPES = {"Allied Health Recovery Request","Clinical Records","Certificate of Capacity","Hospital Discharge Referral"}
EXCLUDE_HANDWRITTEN = {"True"}

def is_excluded(entry):
    return (
        entry.get("documentType") in EXCLUDE_TYPES or
        entry.get("handwritten") in EXCLUDE_HANDWRITTEN 
    )

def split_colon_line_safe(line):
    """Split on first colon not part of time (e.g., 16:30) or ratio (1:2)."""
    match = re.search(r'(?<!\d):(?!\d)', line)
    if not match:
        return None, None
    idx = match.start()
    return line[:idx + 1].strip(), line[idx + 1:].strip()


def format_paragraph(text, bold=False):
    """Wrap text in a <p> tag with tighter spacing, and italicise quoted text."""
    text = re.sub(r'"([^"]+)"', r'<em>"\1"</em>', text)
    if bold:
        text = f"<strong>{text}</strong>"
    return f'<p style="margin: 2px 0;">{text}</p>'


def flush_buffer(buf, out):
    """Append buffer as paragraph and clear it."""
    if buf.strip():
        out.append(format_paragraph(buf.strip()))
    return ""


def clean_html_text(html):
    """Cleans and formats input content into structured HTML."""
    soup = BeautifulSoup(html, "html.parser")
    raw_lines = []

    for p in soup.find_all("p"):
        text = p.get_text(separator=" ", strip=True)
        if text.strip():
            raw_lines.append(text)

    output = []
    buffer = ""
    line_index = 0

    for i, line in enumerate(raw_lines):
        line = line.strip()
        if not line:
            continue

        heading, rest = split_colon_line_safe(line)
        if heading and rest:
            buffer = flush_buffer(buffer, output)
            output.append("<br>")
            output.append(format_paragraph(heading, bold=False))
            buffer = rest
            line_index += 1
            continue

        if line.endswith(":") or re.fullmatch(r"[A-Z\s\-]+:?", line):
            buffer = flush_buffer(buffer, output)
            output.append("<br>")
            output.append(format_paragraph(line, bold=False))
            line_index += 1
            continue

        if re.match(r"^\d+[.)]\s", line):
            buffer = flush_buffer(buffer, output)
            output.append(format_paragraph(line))
            line_index += 1
            continue

        # --- Lookahead for capitalised start on next line ---
        next_line = raw_lines[i + 1].strip() if i + 1 < len(raw_lines) else ""
        next_starts_with_upper = bool(next_line) and next_line[0].isupper()
        next_line_blank = not next_line

        if re.search(r"[.!?]$", line) or next_starts_with_upper or next_line_blank:

            buffer += " " + line
            buffer = flush_buffer(buffer, output)
        else:
            buffer += " " + line

    if buffer.strip():
        output.append(format_paragraph(buffer.strip()))

    return "\n".join(output)


def process_entries(data):
    """Format entryOriginal to entryFinal unless excluded."""
    for entry in data:
        if is_excluded(entry):
            continue  # Leave entryFinal as-is
        if "entryOriginal" in entry and entry["entryOriginal"].strip():
            entry["entryFinal"] = clean_html_text(entry["entryOriginal"])
    return data

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = process_entries(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)

    print(f"Cleaned file written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
