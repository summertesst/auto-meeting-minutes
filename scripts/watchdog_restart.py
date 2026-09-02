"""Optional local watchdog for the caption daemon."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("caption_daemon.py")


def main():
    subprocess.Popen([sys.executable, str(SCRIPT)], cwd=str(SCRIPT.parent))


if __name__ == "__main__":
    main()
