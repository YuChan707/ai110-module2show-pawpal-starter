from typing import List, Optional
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

PREFERENCE_RULES = {
    "no late feeding": lambda t: t.category == "feeding",
    "morning walks":   lambda t: t.category == "walking",
}


class Task:
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        priority: str,
        category: str,
        frequency: str = "daily",
        start_time: str = "08:00",
        due_date: date = None,
    ):
        """Initialize a Task with its name, description, duration, priority, category, frequency, and start time."""
        self.name = name
        self.description = description
        self.duration = duration        # in minutes
        self.priority = priority        # "high", "medium", "low"
        self.category = category        # "feeding", "grooming", "walking", etc.
        self.frequency = frequency      # "daily", "twice daily", "weekly", etc.
        self.start_time = start_time    # "HH:MM" format
        self.due_date = due_date or date.today()
        self.completed = False

    def update_priority(self, new_priority: str) -> None:
        """Validate and update the task's priority level."""
        if new_priority not in PRIORITY_ORDER:
            raise ValueError(f"priority must be one of {list(PRIORITY_ORDER)}")
        self.priority = new_priority

    RECURRENCE_DAYS = {"daily": 1, "twice daily": 1, "weekly": 7}

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and return a new Task for the next occurrence, or None if not recurring."""
        self.completed = True
        days = self.RECURRENCE_DAYS.get(self.frequency)
        if days is None:
            return None
        next_due = self.due_date + timedelta(days=days)
        return Task(
            name=self.name,
            description=self.description,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            start_time=self.start_time,
            due_date=next_due,
        )

    def __repr__(self) -> str:
        """Return a concise string representation showing name, duration, priority, and status."""
        status = "done" if self.completed else "pending"
        return f"Task({self.name!r}, {self.duration}min, priority={self.priority}, {status})"


class Pet:
    def __init__(self, name: str, pet_type: str, age: int):
        """Initialize a Pet with its name, type, and age."""
        self.name = name
        self.pet_type = pet_type        # "dog", "cat", etc.
        self.age = age
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def complete_task(self, task: Task) -> None:
        """Mark a task complete and automatically add the next occurrence if it recurs."""
        next_task = task.mark_complete()
        if next_task:
            self.tasks.append(next_task)

    def __repr__(self) -> str:
        """Return a concise string representation showing name, type, and task count."""
        return f"Pet({self.name!r}, {self.pet_type}, {len(self.tasks)} tasks)"


class Owner:
    def __init__(self, name: str, available_time: int, preferences: List[str] = None):
        """Initialize an Owner with their name, daily time budget, and care preferences."""
        self.name = name
        self.available_time = available_time    # in minutes
        self.preferences = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        results = []
        for pet in self.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    results.append(task)
        return results

    def __repr__(self) -> str:
        """Return a concise string representation showing name, pet count, and time budget."""
        return f"Owner({self.name!r}, {len(self.pets)} pets, {self.available_time}min available)"


class Schedule:
    def __init__(self, tasks: List[Task]):
        """Initialize a Schedule from a list of tasks and compute total time."""
        self.tasks = tasks
        self.total_time = sum(t.duration for t in tasks)  # computed, never out of sync

    def display_plan(self) -> None:
        """Print each scheduled task with a running time tracker."""
        print(f"\n{'='*40}")
        print(f"  Daily Schedule  ({self.total_time} min total)")
        print(f"{'='*40}")
        elapsed = 0
        for i, task in enumerate(self.tasks, start=1):
            print(
                f"{i}. [{task.priority.upper():6}] {task.name} "
                f"({task.duration} min) — {task.category}"
            )
            print(f"   {task.description}")
            elapsed += task.duration
            print(f"   Cumulative time: {elapsed} min")
        print(f"{'='*40}\n")

    def explain_plan(self) -> None:
        """Explain why each task was selected and how it was ordered."""
        print(f"\n{'='*40}")
        print("  Schedule Explanation")
        print(f"{'='*40}")
        for i, task in enumerate(self.tasks, start=1):
            print(
                f"{i}. '{task.name}' was scheduled because it is a "
                f"{task.priority}-priority task (category: {task.category}, "
                f"frequency: {task.frequency})."
            )
        print(f"{'='*40}\n")

    def __repr__(self) -> str:
        """Return a concise string representation showing task count and total duration."""
        return f"Schedule({len(self.tasks)} tasks, {self.total_time} min)"


class Planner:
    def __init__(self, constraints: Optional[dict] = None):
        """Initialize the Planner with an optional dictionary of scheduling constraints."""
        self.constraints = constraints or {}

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high → medium → low), then by duration (shortest first)."""
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER[t.priority], t.duration))

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their start_time in HH:MM format, earliest first."""
        return sorted(tasks, key=lambda t: t.start_time)

    def apply_constraints(self, tasks: List[Task], available_time: int, preferences: List[str] = None) -> List[Task]:
        """Filter tasks by owner preferences, then keep only tasks that fit within available time."""
        if preferences:
            for pref in preferences:
                rule = PREFERENCE_RULES.get(pref)
                if rule:
                    tasks = [t for t in tasks if not rule(t)]

        selected = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration <= available_time:
                selected.append(task)
                time_used += task.duration
        return selected

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return a list of warning strings for any tasks whose time windows overlap."""
        def to_minutes(hhmm: str) -> int:
            """Convert a 'HH:MM' string to total minutes since midnight."""
            h, m = hhmm.split(":")
            return int(h) * 60 + int(m)

        warnings = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                a, b = tasks[i], tasks[j]
                a_start = to_minutes(a.start_time)
                b_start = to_minutes(b.start_time)
                a_end = a_start + a.duration
                b_end = b_start + b.duration
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{a.name}' ({a.start_time}, {a.duration}min) "
                        f"overlaps with '{b.name}' ({b.start_time}, {b.duration}min)"
                    )
        return warnings

    def generate_schedule(self, owner: Owner) -> Schedule:
        """Collect all tasks from the owner's pets, sort, filter, and check for conflicts."""
        all_tasks = owner.get_all_tasks()
        sorted_tasks = self.sort_tasks(all_tasks)
        feasible_tasks = self.apply_constraints(sorted_tasks, owner.available_time, owner.preferences)
        return Schedule(feasible_tasks)
