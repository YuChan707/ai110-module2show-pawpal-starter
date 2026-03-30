import streamlit as st
from pawpal_system import Task, Pet, Owner, Planner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize Owner and Pet in session state once
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time=available_time)
if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, pet_type=species, age=1)
    st.session_state.owner.add_pet(st.session_state.pet)

st.markdown("### Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_description = st.text_input("Description", value="Quick walk around the block")
category = st.text_input("Category", value="walking")

if st.button("Add task"):
    new_task = Task(
        name=task_title,
        description=task_description,
        duration=int(duration),
        priority=priority,
        category=category,
    )
    st.session_state.pet.add_task(new_task)
    st.success(f"Added '{task_title}' to {st.session_state.pet.name}'s tasks.")

current_tasks = st.session_state.pet.tasks
if current_tasks:
    st.write(f"Tasks for {st.session_state.pet.name}:")
    st.table([
        {"title": t.name, "duration (min)": t.duration, "priority": t.priority, "category": t.category}
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    planner = Planner()
    schedule = planner.generate_schedule(st.session_state.owner)
    if schedule.tasks:
        st.success(f"Schedule generated — {schedule.total_time} min of {st.session_state.owner.available_time} min used.")
        st.table([
            {"#": i, "task": t.name, "duration (min)": t.duration, "priority": t.priority, "category": t.category}
            for i, t in enumerate(schedule.tasks, start=1)
        ])
        st.caption(f"Time remaining: {st.session_state.owner.available_time - schedule.total_time} min")
    else:
        st.warning("No tasks fit within the available time.")
