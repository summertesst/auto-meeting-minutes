---
name: semantic-task-confirmation
description: PMO-style semantic confirmation of real meeting action items from raw transcripts.
---

# Semantic Task Confirmation

Use this skill when task detection is inaccurate, context is needed to decide
whether something is an action item, or a meeting uses mixed languages.

## Core standard

A confirmed action item needs:

1. An explicit or unambiguous owner.
2. A concrete future action.
3. A verifiable deliverable or completion target.
4. A deadline, timing signal, or `TBD`.
5. A short genuine quote from the source transcript.
6. An agenda topic.

Classify each candidate:

- `confirmed`: owner, action, and deliverable are clear.
- `possible`: a real action exists, but ownership, deliverable, or timing needs
  human confirmation.
- `rejected`: status, discussion, question, training explanation, conditional
  help, noise, duplicate captions, or wrongly attributed work.

## Seven-stage pipeline

1. **Prepare source:** locate the raw transcript and the matching draft minutes.
2. **Normalize:** remove repeated captions; merge only contextually clear
   fragments.
3. **Understand intent:** label turns as task, status, teaching, question,
   decision, conditional support, or noise.
4. **Extract candidates:** record owner, action, object, timing, and evidence.
5. **Validate owner:** do not confirm an unnamed role or ambiguous speaker.
6. **Validate work:** require a future action and verifiable deliverable; map
   a topic and deadline/TBD.
7. **Finalize:** deduplicate, classify confidence, and record rejected reasons.

## Personal task lists

Include an item in a person's personal task list only when that person is the
explicit or unambiguous owner of a concrete deliverable. Explaining a process,
sharing a screen, or offering help if someone encounters a problem is not a
personal task.

## Output requirements

Update the draft minutes with concise, deliverable-focused task lines:

```text
[T] Owner: Deliverable to be completed; due: YYYY-MM-DD or TBD
[T?] Owner: Candidate deliverable; due: TBD
```

Store a companion audit JSON with five validation-pass summaries, confirmed,
possible, rejected, and personal-task arrays. Every confirmed or possible
entry must include a genuine transcript evidence quote.
