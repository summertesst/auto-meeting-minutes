# Auto Meeting Minutes

[中文说明](README.zh-CN.md)

Windows utility for capturing Microsoft Teams Live Captions locally, generating
structured meeting-minute drafts, and browsing a local meeting archive.

> **Privacy first:** This repository intentionally contains no real transcripts,
> minutes, participant data, organization data, credentials, or generated archive
> content. Read [PRIVACY.md](PRIVACY.md) before use.

## What it does

```text
Teams Live Captions window
        |
        v
Windows UI Automation capture
        |
        v
Local transcript (.txt)
        |
        +--> Draft minutes + local archive site
        |
        +--> Optional Copilot semantic task confirmation
```

The capture daemon detects the Teams Live Captions window, reads its accessible
text through Windows UI Automation, and writes timestamped local transcripts.
At meeting end, it produces a draft minutes file and refreshes the local archive.
Task extraction is deliberately a human/AI semantic review step, not a regex
guessing step.

## Requirements

- Windows 10/11
- Python 3.9+ recommended
- Microsoft Teams with Live Captions enabled
- Permission from participants and your organization to capture/process captions

Install the runtime packages:

```powershell
python -m pip install -r requirements.txt
```

## Quick start

1. Copy `config.example.py` to `scripts\config.py` and adjust it if needed.
2. Create local runtime folders:

   ```powershell
   New-Item -ItemType Directory -Force output\transcripts, output\summaries, site\pages
   ```

3. Start the capture daemon:

   ```powershell
   python scripts\caption_daemon.py
   ```

4. In a Teams meeting, enable Live Captions. The daemon writes local data under
   `output\`.
5. After the meeting, use the semantic task-confirmation workflow to review
   action items, then rebuild the archive:

   ```powershell
   python scripts\build_meeting_site.py
   Start-Process site\index.html
   ```

## Repository layout

| Path | Purpose |
|---|---|
| `scripts\capture_core.py` | Reads the Teams Live Captions accessibility tree. |
| `scripts\caption_daemon.py` | Tray daemon; detects meetings and orchestrates capture. |
| `scripts\summary_generator.py` | Creates a structured **draft** minutes file. |
| `scripts\build_meeting_site.py` | Builds a local archive from local minutes. |
| `scripts\watchdog_restart.py` | Optional Windows watchdog for the daemon. |
| `skills\semantic-task-confirmation\SKILL.md` | PMO-style semantic action-item review rules. |
| `site\` | Blank, static local archive viewer. |
| `examples\` | Fictional sample inputs and outputs. |
| `docs\` | Architecture, workflow, and setup details. |

## Skills and task confirmation

The included `semantic-task-confirmation` skill uses a seven-stage review:

1. Prepare and normalize the raw transcript.
2. Classify speech intent.
3. Extract candidate future actions.
4. Validate ownership.
5. Validate action and deliverable.
6. Validate deadline and topic.
7. Deduplicate and assign `confirmed`, `possible`, or `rejected`.

A confirmed action item must have a clear owner, future action, verifiable
deliverable, source evidence, and agenda topic. A missing deadline is recorded
as `TBD`; it is not automatically a rejection. Personal task lists are limited
to actions explicitly assigned to the selected user.

## Empty website

`site\index.html` opens a safe blank archive page without loading meeting data.
After local minutes are generated, `build_meeting_site.py` creates the ignored
`site\data.js` and `site\pages\` files. Never commit those generated artifacts.

## Publishing safely

Before publishing a fork or derivative, verify:

```powershell
git ls-files
git grep -inE "password|token|secret|@|C:\\Users|transcript|meeting minutes"
```

Review results manually: names, dates, project names, filenames, and meeting
content can all be sensitive even when they do not match these terms.

## License

Released under the [MIT License](LICENSE).
