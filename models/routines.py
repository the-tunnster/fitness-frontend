from dataclasses import dataclass
from typing import List

@dataclass(slots=True)
class Routine:
    user_id: str
    name: str
    id: str

@dataclass(slots=True)
class RoutineExercise:
    exercise_id: str
    name: str
    target_sets: int
    target_reps: int

@dataclass(slots=True)
class FullRoutine:
    id: str
    user_id: str
    name: str
    exercises: List[RoutineExercise]
