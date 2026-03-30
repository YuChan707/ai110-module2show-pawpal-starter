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

# ── 3. Add tasks with different durations to each pet ────────────────────────
dog.add_task(Task("Morning walk",   "30-min walk around the block", 30, "high",   "walking"))
dog.add_task(Task("Feed breakfast", "1 cup dry food in bowl",       10, "high",   "feeding"))
dog.add_task(Task("Grooming",       "Brush coat for 15 minutes",    15, "medium", "grooming"))

cat.add_task(Task("Feed breakfast", "Half can wet food",             5, "high",   "feeding"))
cat.add_task(Task("Litter box",     "Clean and replace litter",     10, "medium", "hygiene",     frequency="twice daily"))
cat.add_task(Task("Playtime",       "Feather wand session",         20, "low",    "enrichment"))

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
print("Suggest a clearer, more readable way to format this schedule output for the terminal")
