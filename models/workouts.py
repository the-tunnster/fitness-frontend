from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Workout:
    id: Optional[str]
    user_id: Optional[str]
    routine_id: Optional[str]
    workout_date: str

@dataclass
class WorkoutSet:
    reps: int
    weight: float

@dataclass
class WorkoutExercise:
    sets: List[WorkoutSet]
    exercise_id: Optional[str]

@dataclass
class FullWorkout:
    user_id: Optional[str]
    routine_id: Optional[str]
    exercises: List[WorkoutExercise]
    workout_date: str
    id: Optional[str]
