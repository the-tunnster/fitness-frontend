from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Routine:
    user_id: Optional[str]
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str
    id: Optional[str]

@dataclass
class RoutineExercise:
    exercise_id: Optional[str]
    name: str
    target_sets: int
    target_reps: List[int]

@dataclass
class FullRoutine:
    id: Optional[str]
    user_id: Optional[str]
    name: str
    description: Optional[str]
    exercises: List[RoutineExercise]
    created_at: str
    updated_at: str
