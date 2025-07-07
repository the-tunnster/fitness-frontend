from dataclasses import dataclass
from typing import List

@dataclass
class Exercise:
    name: str
    category: str
    primary_muscle: str
    secondary_muscle: str
    tertiary_muscle: str
    variation: List[str]
    equipment: List[str]
    id: str

@dataclass
class WorkoutSet:
    reps: int
    weight: float

@dataclass
class ExerciseSets:
    date: str
    equipment: str
    variation: str
    sets: List[WorkoutSet]

@dataclass
class ExerciseHistory:
    id: str
    user_id: str
    exercise_id: str
    exercise_sets: List[ExerciseSets]