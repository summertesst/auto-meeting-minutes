"""Build a local, data-only meeting archive. Generated data is intentionally ignored."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "output" / "summaries"
SITE_DIR = ROOT / "site"


def _field(text, name):
    match = re.search(r"^\s*{}\s*:\s*(.+)$".format(re.escape(name)), text, re.M)
    return match.group(1).strip() if match else ""


def _load_minutes():
    minutes = []
    for path in sorted(SUMMARY_DIR.glob("MeetingMinutes_*.txt"), reverse=True):
        text = path.read_text(encoding="utf-8")
        minutes.append({
            "id": path.stem.lower(),
            "title": _field(text, "Meeting") or "Untitled meeting",
            "date": _field(text, "Date"),
            "time": _field(text, "Time"),
            "fileName": path.name,
            "content": text,
        })
    return minutes


def build_site():
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    minutes = _load_minutes()
    data = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "minutes": minutes,
    }
    (SITE_DIR / "data.js").write_text(
        "window.MEETING_ARCHIVE_DATA = {};\n".format(
            json.dumps(data, ensure_ascii=False)
        ),
        encoding="utf-8",
    )
    print("Built local archive with {} minute files".format(len(minutes)))


if __name__ == "__main__":
    build_site()
