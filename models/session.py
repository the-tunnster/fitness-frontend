from dataclasses import dataclass
from typing import Optional, List

@dataclass
class WorkoutSet:
    reps: int
    weight: float

@dataclass
class WorkoutExercise:
    sets: List[WorkoutSet]
    equipment: str
    variation: str
    exercise_id: str

@dataclass
class WorkoutSession:
    id: Optional[str]
    user_id: Optional[str]
    routine_id: Optional[str]
    exercises: List[WorkoutExercise]
    exercise_index: int
    last_update: str | None