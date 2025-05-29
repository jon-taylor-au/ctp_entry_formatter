import json
import re
from bs4 import BeautifulSoup
from pathlib import Path

# --- Config ---
INPUT_FILE = Path("outputs/json_exports/chronology.json")
OUTPUT_FILE = Path("outputs/json_exports/chronology_writeback.json")


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

    for line in raw_lines:
        line = line.strip()
        if not line:
            continue

        heading, rest = split_colon_line_safe(line)
        if heading and rest:
            buffer = flush_buffer(buffer, output)
            output.append("<br>")
            output.append(format_paragraph(heading, bold=True))
            buffer = rest
            line_index += 1
            continue

        if line.endswith(":"):
            buffer = flush_buffer(buffer, output)
            output.append("<br>")
            output.append(format_paragraph(line, bold=True))
            line_index += 1
            continue

        if re.fullmatch(r"[A-Z\s\-]+:?", line):
            buffer = flush_buffer(buffer, output)
            output.append("<br>")
            output.append(format_paragraph(line, bold=True))
            line_index += 1
            continue

        if re.match(r"^\d+[.)]\s", line):
            buffer = flush_buffer(buffer, output)
            output.append(format_paragraph(line))
            line_index += 1
            continue

        if re.search(r"[.!?]$", line):
            buffer += " " + line
            buffer = flush_buffer(buffer, output)
        else:
            buffer += " " + line

        if line_index == 0 and output:
            output.append("<br>")
            line_index += 1

    if buffer.strip():
        output.append(format_paragraph(buffer.strip()))

    return "\n".join(output)


def process_entries(data):
    """Process each entry's `entryOriginal` content and store in `entryFinal`."""
    for entry in data:
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
