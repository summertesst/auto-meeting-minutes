"""Generate structured local meeting-minute drafts from a caption transcript."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def _metadata(transcript_path):
    title = "Teams meeting"
    lines = transcript_path.read_text(encoding="utf-8").splitlines()
    for line in lines[:10]:
        if line.startswith("# Window:"):
            parts = [part.strip() for part in line.split("|")]
            if len(parts) >= 2:
                title = parts[1] or title
    timestamps = re.findall(r"^\[(\d{2}:\d{2}:\d{2})\]$", "\n".join(lines), re.M)
    return title, (timestamps[0] if timestamps else "unknown"), (timestamps[-1] if timestamps else "unknown")


def generate_summary_txt(transcript_file, output_dir):
    """Write a draft minutes file. Semantic task review happens separately."""
    transcript_path = Path(transcript_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    title, start, end = _metadata(transcript_path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    minutes_path = output_dir / "MeetingMinutes_{}.txt".format(stamp)
    date = datetime.now().strftime("%Y-%m-%d")
    minutes_path.write_text(
        "\n".join([
            "=" * 80,
            "  MEETING MINUTES — Auto-Captured (Tasks: pending AI analysis)",
            "=" * 80,
            "  Meeting : {}".format(title),
            "  Date    : {}".format(date),
            "  Time    : {} — {}".format(start, end),
            "  Source  : {}".format(transcript_path.name),
            "",
            "=" * 80,
            "  ACTION ITEMS",
            "=" * 80,
            "",
            "  Task extraction is intentionally pending semantic AI/human review.",
            "  Review the source transcript before recording confirmed action items.",
            "",
        ]),
        encoding="utf-8",
    )
    return str(minutes_path)
