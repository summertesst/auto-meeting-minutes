"""Copy this file to scripts/config.py and set paths for your computer."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts"
SUMMARIES_DIR = OUTPUT_DIR / "summaries"
SITE_DIR = PROJECT_ROOT / "site"

# Change only when your environment needs a specific Python executable.
PYTHON_EXE = sys.executable
