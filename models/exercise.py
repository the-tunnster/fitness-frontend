from dataclasses import dataclass
from typing import List

@dataclass(slots=True)
class Exercise:
    name: str
    category: str
    variations: List[str]
    equipment: List[str]
    id: str

@dataclass(slots=True)
class WorkoutSet:
    reps: int
    weight: float

@dataclass(slots=True)
class ExerciseSets:
    date: str
    equipment: str
    variation: str
    sets: List[WorkoutSet]

@dataclass(slots=True)
class ExerciseHistory:
    id: str
    user_id: str
    exercise_id: str
    exercise_sets: List[ExerciseSets]