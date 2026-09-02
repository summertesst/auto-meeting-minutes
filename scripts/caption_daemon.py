"""Windows tray daemon that captures a Teams Live Captions window locally."""
from __future__ import annotations

import threading
import time
from datetime import datetime
from pathlib import Path

import pystray
from PIL import Image, ImageDraw

from capture_core import append_new_captions, find_teams_caption_window, read_captions_uia
from summary_generator import generate_summary_txt
from build_meeting_site import build_site

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = ROOT / "output" / "transcripts"
SUMMARIES_DIR = ROOT / "output" / "summaries"
POLL_SECONDS = 5


class CaptionDaemon:
    def __init__(self):
        self.capture_file = None
        self.known_entries = set()
        self.in_call = False
        self.icon = None

    def _start(self, title):
        TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        filename = "LiveCaption_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.capture_file = TRANSCRIPTS_DIR / filename
        self.capture_file.write_text(
            "# Teams Live Caption (UIA) - {}\n# Window: {}\n".format(
                datetime.now().strftime("%Y-%m-%d %H:%M"), title
            ),
            encoding="utf-8",
        )
        self.known_entries.clear()
        self.in_call = True
        self.icon.notify("Capturing Teams Live Captions locally.", "Auto Meeting Minutes")

    def _finish(self):
        if not self.capture_file:
            return
        generate_summary_txt(self.capture_file, SUMMARIES_DIR)
        build_site()
        self.icon.notify(
            "Draft minutes created. Review tasks semantically before sharing.",
            "Auto Meeting Minutes",
        )
        self.capture_file = None
        self.in_call = False

    def monitor(self):
        while True:
            window = find_teams_caption_window()
            if window and not self.in_call:
                self._start(window[1])
            elif not window and self.in_call:
                self._finish()
            elif window and self.in_call:
                try:
                    captions = read_captions_uia(window[0])
                    self.known_entries = append_new_captions(
                        self.capture_file, captions, self.known_entries
                    )
                except Exception as exc:
                    print("Caption read failed: {}".format(exc))
            time.sleep(POLL_SECONDS)


def _icon_image():
    image = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill=(31, 111, 235, 255))
    draw.rectangle((28, 20, 36, 44), fill=(255, 255, 255, 255))
    return image


def main():
    daemon = CaptionDaemon()
    menu = pystray.Menu(pystray.MenuItem("Quit", lambda icon, item: icon.stop()))
    daemon.icon = pystray.Icon("auto-meeting-minutes", _icon_image(), "Auto Meeting Minutes", menu)
    threading.Thread(target=daemon.monitor, daemon=True).start()
    daemon.icon.run()


if __name__ == "__main__":
    main()
