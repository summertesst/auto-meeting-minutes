# Architecture

## Active local pipeline

```text
Teams Live Captions
  -> capture_core.py
  -> caption_daemon.py
  -> output/transcripts/LiveCaption_*.txt
  -> summary_generator.py
  -> output/summaries/MeetingMinutes_*.txt
  -> build_meeting_site.py
  -> site/index.html + ignored generated archive files
```

`capture_core.py` uses Windows UI Automation instead of screenshots. It reads
the text tree exposed by the pinned Live Captions window, filters interface
noise, identifies speakers, and de-duplicates repeated caption updates.

`caption_daemon.py` is the long-running Windows tray process. It starts capture
when the Live Captions window appears, stops after the window closes, generates
draft minutes, refreshes the local site, and opens the local archive.

`summary_generator.py` intentionally does not decide action items from regex
patterns. It creates a structured draft. The semantic task-confirmation skill
is the authoritative task-review step.

## Boundaries

- **Local capture boundary:** captions and minutes remain in `output/`.
- **Semantic review boundary:** an AI/user reviews tasks from the full raw
  transcript and records evidence in a separate audit file.
- **Presentation boundary:** the static site only reads local generated data.
- **Repository boundary:** `.gitignore` prevents runtime data from being
  committed.
