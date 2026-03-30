# app.py
# Streamlit UI layer for PawPal+.
# This file only handles user input and display — all scheduling logic
# lives in pawpal_system.py so it can be tested independently via main.py.

import streamlit as st
from pawpal_system import Task, Pet, Owner, Planner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── 1. Owner & Pet Setup ──────────────────────────────────────────────────────
st.subheader("Owner & Pet Setup")

owner_name     = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=90)
pet_name       = st.text_input("Pet name", value="Mochi")
species        = st.selectbox("Species", ["dog", "cat", "other"])
preferences    = st.multiselect(
    "Owner preferences",
    options=["no late feeding", "morning walks"],
    default=[],
)

# The "Save" button recreates Owner and Pet from the current input values.
# This is intentional — it lets the user change the setup and regenerate
# without the old frozen objects persisting from a previous session.
if st.button("Save owner & pet"):
    st.session_state.owner = Owner(
        name=owner_name,
        available_time=int(available_time),
        preferences=preferences,
    )
    # Create a fresh Pet and immediately link it to the new Owner.
    pet = Pet(name=pet_name, pet_type=species, age=1)
    st.session_state.pet = pet
    st.session_state.owner.add_pet(pet)
    # Clear any previously generated schedule so the UI stays consistent
    # with the new owner/pet configuration.
    st.session_state.schedule = None
    st.success(f"Saved {owner_name} with pet {pet_name}.")

# Guard: stop rendering the rest of the page until owner is saved.
# st.stop() halts script execution for this rerun — nothing below runs.
# This prevents KeyError crashes when session_state.pet doesn't exist yet.
if "owner" not in st.session_state:
    st.info("Fill in owner & pet details above, then click **Save owner & pet** to continue.")
    st.stop()

st.divider()

# ── 2. Add a Task ─────────────────────────────────────────────────────────────
st.subheader(f"Add a Task for {st.session_state.pet.name}")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    # index=2 defaults to "high" — most pet care tasks are high priority.
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5, col6 = st.columns(3)
with col4:
    task_description = st.text_input("Description", value="Quick walk around the block")
with col5:
    category = st.text_input("Category", value="walking")
with col6:
    # start_time drives conflict detection and sort_by_time() — must be "HH:MM".
    start_time = st.text_input("Start time (HH:MM)", value="08:00")

# frequency feeds into RECURRENCE_DAYS so mark_complete() knows when to reschedule.
frequency = st.selectbox("Frequency", ["daily", "twice daily", "weekly"], index=0)

if st.button("Add task"):
    new_task = Task(
        name=task_title,
        description=task_description,
        duration=int(duration),
        priority=priority,
        category=category,
        frequency=frequency,
        start_time=start_time,
    )
    # add_task() appends to the Pet's task list, which the Owner can later
    # retrieve via get_all_tasks() for scheduling.
    st.session_state.pet.add_task(new_task)
    # Reset the schedule — it is now stale because the task list changed.
    st.session_state.schedule = None
    st.success(f"Added '{task_title}' to {st.session_state.pet.name}'s tasks.")

# Display the current task list so the user can see what has been added.
current_tasks = st.session_state.pet.tasks
if current_tasks:
    st.write(f"**{st.session_state.pet.name}'s tasks ({len(current_tasks)} total):**")
    st.table([
        {
            "task": t.name,
            "start": t.start_time,
            "duration (min)": t.duration,
            "priority": t.priority,
            "category": t.category,
            "frequency": t.frequency,
            # Show a checkmark for completed tasks so the user can see status at a glance.
            "done": "✓" if t.completed else "",
        }
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── 3. Generate Schedule ──────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    planner  = Planner()
    # generate_schedule() runs the full pipeline:
    # collect → sort by priority → filter by preference + time → return Schedule.
    schedule = planner.generate_schedule(st.session_state.owner)
    # detect_conflicts() checks ALL tasks (not just scheduled ones) so the owner
    # is warned about overlaps even if a task was filtered out of the schedule.
    conflicts = planner.detect_conflicts(st.session_state.owner.get_all_tasks())
    # Store both in session_state so they persist across reruns.
    # Without this, clicking any other widget would wipe the results.
    st.session_state.schedule  = schedule
    st.session_state.conflicts = conflicts

# Render the persisted schedule — this block runs on every rerun so the
# schedule stays visible even when the user interacts with other widgets.
if st.session_state.get("schedule"):
    schedule = st.session_state.schedule
    owner    = st.session_state.owner

    st.success(f"Schedule generated — {schedule.total_time} min of {owner.available_time} min used.")
    st.table([
        {
            "#": i,
            "task": t.name,
            "start": t.start_time,
            "duration (min)": t.duration,
            "priority": t.priority,
            "category": t.category,
        }
        for i, t in enumerate(schedule.tasks, start=1)
    ])
    st.caption(f"Time remaining: {owner.available_time - schedule.total_time} min")

    # Explanation expander — mirrors Schedule.explain_plan() for the UI.
    # Helps the owner understand WHY each task was included.
    with st.expander("Why was each task chosen?"):
        for i, t in enumerate(schedule.tasks, start=1):
            st.markdown(
                f"**{i}. {t.name}** — `{t.priority}` priority · "
                f"`{t.category}` · repeats `{t.frequency}`"
            )

    # Conflict warnings — shown only when detect_conflicts() found overlaps.
    # Returning strings (not raising exceptions) keeps the app alive so the
    # owner can see the issue and decide how to fix it.
    if st.session_state.get("conflicts"):
        st.divider()
        st.warning("⚠️ Scheduling conflicts detected:")
        for w in st.session_state.conflicts:
            st.markdown(f"- {w}")
    else:
        st.info("No scheduling conflicts found.")
