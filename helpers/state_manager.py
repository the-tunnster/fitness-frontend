import streamlit as st
from typing import Optional, List, Any
from dataclasses import dataclass, field

# --- IMPORTS ---
from models.user import BasicUser, FullUser
from models.session import WorkoutSession
# from models.routines import FullRoutine (If needed later)

@dataclass
class BuilderExercise:
    """Represents a single row in the routine editor/creator."""
    name: str
    sets: int
    reps: int
    remove: bool = False

@dataclass
class RoutineBuilder:
    """
    Rich Model for managing the state of a routine being created or edited.
    Encapsulates list manipulation logic.
    """
    name: str = ""
    description: str = ""
    exercises: List[BuilderExercise] = field(default_factory=lambda: [])

    def add_exercise(self, default_name: str, default_sets: int = 3, default_reps: int = 10):
        self.exercises.append(BuilderExercise(name=default_name, sets=default_sets, reps=default_reps))

    def remove_flagged(self):
        """Removes all exercises marked for removal."""
        self.exercises = [ex for ex in self.exercises if not ex.remove]

    def clear(self):
        self.name = ""
        self.description = ""
        self.exercises = []

class AppState:
    """
    Strongly-typed proxy for streamlit.session_state.
    """
    
    # --- Constants ---
    KEY_USER = "user_data"
    KEY_USER_FULL = "user_full_data"
    KEY_ROUTINE_CREATOR = "routine_creator_data"
    KEY_ROUTINE_EDITOR = "routine_editor_data"
    KEY_WORKOUT_SESSION = "workout_session_data"
    KEY_EXERCISE_IDX = "current_exercise_index"
    KEY_ADD_DIALOG = "add_exercise_dialog"
    KEY_EXERCISE_SELECTION = "workout_exercise_selection"

    def __init__(self):
        self._ensure_key(self.KEY_USER, None)
        self._ensure_key(self.KEY_USER_FULL, None)
        # Initialize builders as None; pages will create them if needed
        self._ensure_key(self.KEY_ROUTINE_CREATOR, None)
        self._ensure_key(self.KEY_ROUTINE_EDITOR, None)
        self._ensure_key(self.KEY_WORKOUT_SESSION, None)
        self._ensure_key(self.KEY_EXERCISE_IDX, 0)
        self._ensure_key(self.KEY_ADD_DIALOG, False)
        self._ensure_key(self.KEY_EXERCISE_SELECTION, None)

    def _ensure_key(self, key: str, default: Any):
        if key not in st.session_state:
            st.session_state[key] = default

    # --- Type-Safe Properties ---

    @property
    def user(self) -> Optional[BasicUser]:
        return st.session_state[self.KEY_USER]

    @user.setter
    def user(self, value: Optional[BasicUser]):
        st.session_state[self.KEY_USER] = value

    @property
    def full_user(self) -> Optional[FullUser]:
        return st.session_state[self.KEY_USER_FULL]
    
    @full_user.setter
    def full_user(self, value: Optional[FullUser]):
        st.session_state[self.KEY_USER_FULL] = value

    @property
    def workout_session(self) -> Optional[WorkoutSession]:
        return st.session_state[self.KEY_WORKOUT_SESSION]

    @workout_session.setter
    def workout_session(self, value: Optional[WorkoutSession]):
        st.session_state[self.KEY_WORKOUT_SESSION] = value

    @property
    def routine_creator(self) -> Optional[RoutineBuilder]:
        return st.session_state[self.KEY_ROUTINE_CREATOR]

    @routine_creator.setter
    def routine_creator(self, value: Optional[RoutineBuilder]):
        st.session_state[self.KEY_ROUTINE_CREATOR] = value

    @property
    def routine_editor(self) -> Optional[RoutineBuilder]:
        return st.session_state[self.KEY_ROUTINE_EDITOR]

    @routine_editor.setter
    def routine_editor(self, value: Optional[RoutineBuilder]):
        st.session_state[self.KEY_ROUTINE_EDITOR] = value

    @property
    def current_exercise_index(self) -> int:
        return st.session_state[self.KEY_EXERCISE_IDX]

    @current_exercise_index.setter
    def current_exercise_index(self, value: int):
        st.session_state[self.KEY_EXERCISE_IDX] = value

    @property
    def is_add_dialog_open(self) -> bool:
        return st.session_state[self.KEY_ADD_DIALOG]

    @is_add_dialog_open.setter
    def is_add_dialog_open(self, value: bool):
        st.session_state[self.KEY_ADD_DIALOG] = value

    @property
    def workout_exercise_selection(self) -> Any:
        return st.session_state[self.KEY_EXERCISE_SELECTION]

    @workout_exercise_selection.setter
    def workout_exercise_selection(self, value: Any):
        st.session_state[self.KEY_EXERCISE_SELECTION] = value

    # --- Helper Actions ---

    def reset_workout_state(self):
        """Specific helper to clear workout-related data."""
        self.workout_session = None
        self.current_exercise_index = 0
        self.is_add_dialog_open = False
        self.workout_exercise_selection = None

    # --- Helper Actions ---

    def get_or_create_routine_creator(self) -> RoutineBuilder:
        if self.routine_creator is None:
            self.routine_creator = RoutineBuilder()
        return self.routine_creator

    def get_or_create_routine_editor(self) -> RoutineBuilder:
        if self.routine_editor is None:
            self.routine_editor = RoutineBuilder()
        return self.routine_editor

    def clear_keys(self, keys: List[str]):
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
        self.__init__()