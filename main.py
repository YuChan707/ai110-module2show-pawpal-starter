from pawpal_system import Task, Pet, Owner, Planner

# ── 1. Create an owner ────────────────────────────────────────────────────────
owner = Owner(
    name="Jordan",
    available_time=60,
    preferences=["morning walks", "no late feeding"],
)

# ── 2. Create pets ────────────────────────────────────────────────────────────
dog = Pet(name="Mochi", pet_type="dog", age=3)
cat = Pet(name="Luna",  pet_type="cat", age=5)

# ── 3. Add tasks to the dog ───────────────────────────────────────────────────
dog.add_task(Task("Morning walk",   "30-min walk around the block", 30, "high",   "walking"))
dog.add_task(Task("Feed breakfast", "1 cup dry food in bowl",       10, "high",   "feeding"))
dog.add_task(Task("Grooming",       "Brush coat for 15 minutes",    15, "medium", "grooming"))

# ── 4. Add tasks to the cat ───────────────────────────────────────────────────
cat.add_task(Task("Feed breakfast", "Half can wet food",            5,  "high",   "feeding"))
cat.add_task(Task("Litter box",     "Clean and replace litter",     10, "medium", "hygiene", frequency="twice daily"))
cat.add_task(Task("Playtime",       "Feather wand session",         20, "low",    "enrichment"))

# ── 5. Register pets with the owner ──────────────────────────────────────────
owner.add_pet(dog)
owner.add_pet(cat)

# ── 6. Run the planner ────────────────────────────────────────────────────────
planner = Planner()
schedule = planner.generate_schedule(owner)

# ── 7. Display results ────────────────────────────────────────────────────────
print(f"Owner  : {owner}")
print(f"Pets   : {owner.pets}")
print(f"Schedule: {schedule}")

schedule.display_plan()
schedule.explain_plan()

# ── 8. Edge case: not enough time for any tasks ───────────────────────────────
print("--- Edge case: only 5 minutes available ---")
tight_owner = Owner("Alex", available_time=5, preferences=[])
tight_pet   = Pet("Buddy", "dog", 2)
tight_pet.add_task(Task("Long walk", "60-min hike", 60, "high", "walking"))
tight_owner.add_pet(tight_pet)

tight_schedule = planner.generate_schedule(tight_owner)
if not tight_schedule.tasks:
    print("No tasks fit within the available time.\n")
else:
    tight_schedule.display_plan()

# ── 9. Test update_priority ───────────────────────────────────────────────────
print("--- Test: update_priority ---")
task = dog.tasks[2]  # Grooming (medium)
print(f"Before: {task}")
task.update_priority("high")
print(f"After : {task}")

# ── 10. Test mark_complete ────────────────────────────────────────────────────
print("\n--- Test: mark_complete ---")
dog.tasks[0].mark_complete()
print(f"Morning walk status: {dog.tasks[0]}")
