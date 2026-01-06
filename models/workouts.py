from dataclasses import dataclass
from typing import Optional, List

@dataclass(slots=True)
class Workout:
    id: Optional[str]
    user_id: Optional[str]
    routine_id: Optional[str]
    workout_date: str

@dataclass(slots=True)
class WorkoutSet:
    reps: int
    weight: float

@dataclass(slots=True)
class WorkoutExercise:
    sets: List[WorkoutSet]
    exercise_id: Optional[str]

@dataclass(slots=True)
class FullWorkout:
    user_id: Optional[str]
    routine_id: Optional[str]
    exercises: List[WorkoutExercise]
    workout_date: str
    id: Optional[str]
