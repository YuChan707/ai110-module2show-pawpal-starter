from typing import List, Optional


class Task:
    def __init__(self, name: str, duration: int, priority: str, category: str):
        self.name = name
        self.duration = duration        # in minutes
        self.priority = priority        # "high", "medium", "low"
        self.category = category        # "feeding", "grooming", "walking", etc.

    def update_priority(self, new_priority: str) -> None:
        raise NotImplementedError


class Pet:
    def __init__(self, name: str, type: str, age: int):
        self.name = name
        self.type = type                # "dog", "cat", etc.
        self.age = age
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        raise NotImplementedError


class Owner:
    def __init__(self, name: str, available_time: int, preferences: str):
        self.name = name
        self.available_time = available_time    # in minutes
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError


class Schedule:
    def __init__(self, tasks: List[Task], total_time: int):
        self.tasks = tasks
        self.total_time = total_time

    def display_plan(self) -> None:
        raise NotImplementedError

    def explain_plan(self) -> None:
        raise NotImplementedError


class Planner:
    def __init__(self, constraints: Optional[dict] = None):
        self.constraints = constraints or {}

    def generate_schedule(self, tasks: List[Task], available_time: int) -> Schedule:
        raise NotImplementedError

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        raise NotImplementedError

    def apply_constraints(self, tasks: List[Task], available_time: int) -> List[Task]:
        raise NotImplementedError
