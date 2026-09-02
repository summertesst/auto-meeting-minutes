"""Read Microsoft Teams Live Captions through Windows UI Automation."""
from __future__ import annotations

import re
from datetime import datetime

import win32gui

NOISE_LABELS = {
    "Live Captions",
    "Caption settings",
    "Unpin window",
    "Settings and more",
    "Minimize",
    "Maximize",
    "Close",
}

SPEAKER_RE = re.compile(
    r"^[A-Za-z][^,]{1,40},\s*[A-Za-z][^()]{0,40}(?:\([^)]{2,60}\))?$"
)


def find_teams_caption_window():
    """Return the first pinned Teams Live Captions window, if one is open."""
    found = []

    def collect(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if "Microsoft Teams" in title and ("Live Caption" in title or "Captions" in title):
            found.append((hwnd, title))

    win32gui.EnumWindows(collect, None)
    return found[0] if found else None


def _clean(text):
    text = (text or "").strip()
    for label in NOISE_LABELS:
        text = text.replace(label, "")
    return " ".join(text.split())


def _is_speaker(text):
    return bool(SPEAKER_RE.fullmatch(text)) and len(text) < 100


def read_captions_uia(hwnd):
    """Return deduplicated ``(speaker, caption)`` pairs from a caption window."""
    from pywinauto import Application

    app = Application(backend="uia").connect(handle=hwnd)
    texts = [_clean(element.window_text()) for element in app.window(handle=hwnd).descendants()]
    texts = [text for text in texts if text]

    entries = []
    speaker = ""
    for text in texts:
        if _is_speaker(text):
            speaker = text
        elif speaker and text not in NOISE_LABELS:
            entry = (speaker, text)
            if entry not in entries:
                entries.append(entry)
    return entries


def append_new_captions(path, captions, known_entries):
    """Append only unseen captions and return the updated known-entry set."""
    if not captions:
        return known_entries

    with open(path, "a", encoding="utf-8") as handle:
        for speaker, text in captions:
            key = "{}\n{}".format(speaker, text)
            if key in known_entries:
                continue
            known_entries.add(key)
            handle.write("\n[{}]\n{}: {}\n".format(
                datetime.now().strftime("%H:%M:%S"), speaker, text
            ))
    return known_entries
