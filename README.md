# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler has been extended beyond basic priority + time filtering with four new features:

**Preference-aware filtering** — `Owner.preferences` (e.g. `"no late feeding"`, `"morning walks"`) are now mapped to real filter rules in `PREFERENCE_RULES`. Tasks that violate a preference are removed from the pool before time-budgeting runs.

**Time-based sorting** — `Planner.sort_by_time()` orders any task list by `start_time` in `"HH:MM"` format using a lambda key on Python's `sorted()`. Because `"HH:MM"` strings sort correctly as plain strings, no date parsing is needed.

**Auto-rescheduling** — `Task.mark_complete()` now returns a new `Task` instance due on the next occurrence (`today + timedelta(days=1)` for daily, `+7` for weekly). `Pet.complete_task()` calls this and automatically appends the new task, so recurring care never falls off the list.

**Conflict detection** — `Planner.detect_conflicts()` checks every pair of tasks for overlapping time windows using the interval formula `a_start < b_end and b_start < a_end`. It returns a list of human-readable warning strings rather than raising an exception, so the app stays running and the owner is informed.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
