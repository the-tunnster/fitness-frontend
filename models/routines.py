from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Routine:
    user_id: Optional[str]
    name: str
    id: Optional[str]

@dataclass
class RoutineExercise:
    exercise_id: Optional[str]
    name: str
    target_sets: int
    target_reps: int

@dataclass
class FullRoutine:
    id: Optional[str]
    user_id: Optional[str]
    name: str
    exercises: List[RoutineExercise]
