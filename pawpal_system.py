from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Task:
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        priority: str,
        category: str,
        frequency: str = "daily",
    ):
        """Initialize a Task with its name, description, duration, priority, category, and frequency."""
        self.name = name
        self.description = description
        self.duration = duration        # in minutes
        self.priority = priority        # "high", "medium", "low"
        self.category = category        # "feeding", "grooming", "walking", etc.
        self.frequency = frequency      # "daily", "twice daily", "weekly", etc.
        self.completed = False

    def update_priority(self, new_priority: str) -> None:
        """Validate and update the task's priority level."""
        if new_priority not in PRIORITY_ORDER:
            raise ValueError(f"priority must be one of {list(PRIORITY_ORDER)}")
        self.priority = new_priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def __repr__(self) -> str:
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

    def __repr__(self) -> str:
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

    def __repr__(self) -> str:
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
        return f"Schedule({len(self.tasks)} tasks, {self.total_time} min)"


class Planner:
    def __init__(self, constraints: Optional[dict] = None):
        """Initialize the Planner with an optional dictionary of scheduling constraints."""
        self.constraints = constraints or {}

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high → medium → low), then by duration (shortest first)."""
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER[t.priority], t.duration))

    def apply_constraints(self, tasks: List[Task], available_time: int) -> List[Task]:
        """Keep only tasks that fit within the owner's available time."""
        selected = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration <= available_time:
                selected.append(task)
                time_used += task.duration
        return selected

    def generate_schedule(self, owner: Owner) -> Schedule:
        """Collect all tasks from the owner's pets, sort and filter them, return a Schedule."""
        all_tasks = owner.get_all_tasks()
        sorted_tasks = self.sort_tasks(all_tasks)
        feasible_tasks = self.apply_constraints(sorted_tasks, owner.available_time)
        return Schedule(feasible_tasks)
