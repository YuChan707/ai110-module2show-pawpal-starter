from pawpal_system import Task, Pet, Owner, Planner

# ── 1. Create an owner ────────────────────────────────────────────────────────
owner = Owner(
    name="Jordan",
    available_time=90,
    preferences=["morning walks", "no late feeding"],
    
)   

# ── 2. Create two pets ────────────────────────────────────────────────────────
dog = Pet(name="Mochi", pet_type="dog", age=3)
cat = Pet(name="Luna",  pet_type="cat", age=5)

# ── 3. Add tasks OUT OF ORDER (mixed start_times) to demo sort_by_time ───────
dog.add_task(Task("Grooming",       "Brush coat for 15 minutes",    15, "medium", "grooming",  start_time="10:00"))
dog.add_task(Task("Morning walk",   "30-min walk around the block", 30, "high",   "walking",   start_time="07:00"))
dog.add_task(Task("Feed breakfast", "1 cup dry food in bowl",       10, "high",   "feeding",   start_time="08:00"))

cat.add_task(Task("Playtime",       "Feather wand session",         20, "low",    "enrichment",start_time="15:00"))
cat.add_task(Task("Feed breakfast", "Half can wet food",             5, "high",   "feeding",   start_time="08:30"))
cat.add_task(Task("Litter box",     "Clean and replace litter",     10, "medium", "hygiene",   frequency="twice daily", start_time="09:00"))

# ── 4. Register pets with the owner ──────────────────────────────────────────
owner.add_pet(dog)
owner.add_pet(cat)

# ── 5. Generate the schedule ──────────────────────────────────────────────────
planner  = Planner()
schedule = planner.generate_schedule(owner)

# ── 6. Print Today's Schedule ─────────────────────────────────────────────────
print(f"\nOwner : {owner.name}  |  Time budget: {owner.available_time} min")
print(f"Pets  : {', '.join(p.name for p in owner.pets)}")
print()

print("Today's Schedule")
print("=" * 40)
elapsed = 0
for i, task in enumerate(schedule.tasks, start=1):
    elapsed += task.duration
    print(f"{i}. {task.name:<20} {task.duration:>3} min  [{task.priority}]")
    print(f"   {task.description}")
print("-" * 40)
print(f"   Total time used : {schedule.total_time} min")
print(f"   Time remaining  : {owner.available_time - schedule.total_time} min")
print("=" * 40)

# ── 7. Sort all tasks by start_time ──────────────────────────────────────────
all_tasks = owner.get_all_tasks()
sorted_by_time = planner.sort_by_time(all_tasks)

print("\nAll Tasks Sorted by Start Time")
print("=" * 40)
for t in sorted_by_time:
    print(f"  {t.start_time}  {t.name:<20} [{t.priority}]")
print("=" * 40)

# ── 8. Mark some tasks complete then filter ───────────────────────────────────
dog.tasks[0].mark_complete()   # Grooming → done
cat.tasks[2].mark_complete()   # Litter box → done

print("\nPending tasks (all pets):")
for t in owner.filter_tasks(completed=False):
    print(f"  - {t.name} [{t.priority}]")

print("\nCompleted tasks (all pets):")
for t in owner.filter_tasks(completed=True):
    print(f"  - {t.name} [{t.priority}]")

print("\nMochi's tasks only:")
for t in owner.filter_tasks(pet_name="Mochi"):
    status = "done" if t.completed else "pending"
    print(f"  - {t.name} ({status})")
