# Workflow

## 1. Capture

Enable Live Captions in Microsoft Teams. Start the daemon before the meeting.
It detects the caption window, reads accessible caption text, and writes a
timestamped transcript under `output/transcripts/`.

## 2. Draft minutes

When the caption window closes, the daemon invokes the local minutes generator.
The output is a draft minutes file in `output/summaries/`. The draft is marked
as pending semantic task analysis.

## 3. Confirm action items

Use the `semantic-task-confirmation` skill on the raw transcript. Confirmed
items must include:

- owner
- concrete future action
- verifiable deliverable
- deadline or `TBD`
- short real evidence quote
- agenda topic

Classify unclear candidates as `possible`; reject status updates, questions,
screen-sharing instructions, duplicated captions, and conditional support.

## 4. Build and browse

Run:

```powershell
python scripts\build_meeting_site.py
Start-Process site\index.html
```

The website groups local minutes by date. It is intentionally blank in a fresh
clone and becomes populated only from your own local runtime data.

## 5. Retention

Delete or archive files in `output/` according to your organization's approved
retention policy. Do not add the directory to Git.
