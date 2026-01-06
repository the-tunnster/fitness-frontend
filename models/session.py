from dataclasses import dataclass
from typing import Optional, List

@dataclass(slots=True)
class WorkoutSet:
    reps: int
    weight: float

@dataclass(slots=True)
class WorkoutExercise:
    sets: List[WorkoutSet]
    equipment: str
    variation: str
    exercise_id: str
    name: str

    @property
    def display_name(self) -> str:
        return f"{self.name} | {self.variation}, {self.equipment}"

    def add_set(self, reps: int, weight: float):
        self.sets.append(WorkoutSet(reps=reps, weight=weight))

    def drop_set(self):
        if self.sets:
            self.sets.pop()

@dataclass(slots=True)
class WorkoutSession:
    id: Optional[str]
    user_id: Optional[str]
    routine_id: Optional[str]
    exercises: List[WorkoutExercise]
    exercise_index: int
    last_update: str | None

    @property
    def current_exercise(self) -> Optional[WorkoutExercise]:
        if 0 <= self.exercise_index < len(self.exercises):
            return self.exercises[self.exercise_index]
        return None

    def add_exercise(self, exercise: WorkoutExercise):
        self.exercises.append(exercise)
        self.exercise_index = len(self.exercises) - 1