import streamlit
from helpers.state_manager import AppState
from helpers.user_interface import *
from database.read import getBasicUser, getExerciseList, getExerciseIDs
from database.create import createUserRoutine
from models.routines import RoutineExercise, FullRoutine

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
state = AppState()

# --- Auth Check ---
if state.user is None:
    state.user = getBasicUser(str(streamlit.user.email))
if state.user is None or state.user.clearance_level < 1:
    accessControlWarning()
    getInTouch()
    streamlit.stop()
user_data = state.user

streamlit.title("Routine Creation", anchor=False)
streamlit.divider()

# --- Load State (Rich Object) ---
# Use the helper to ensure we get a valid RoutineBuilder object
routine = state.get_or_create_routine_creator()

# --- UI Logic ---
routine.name = streamlit.text_input(
    label="Routine Name",
    value=routine.name,
    placeholder="Routine Name",
    label_visibility="collapsed"
)

# Fetch global list for the dropdowns
global_exercise_list = getExerciseList() or []
global_exercise_names = [ex.name for ex in global_exercise_list] or ["None"]

with streamlit.form("routine_creator_form", clear_on_submit=False, enter_to_submit=False, border=False):
    # Header
    h1, h2 = streamlit.columns([1, 1], vertical_alignment="bottom")
    h3, h4, h5 = h2.columns([1, 1, 1], vertical_alignment="bottom")
    h1.write("Exercise Name")
    h3.write("Sets")
    h4.write("Reps")

    # Render Rows
    for i, exercise in enumerate(routine.exercises):
        c1, c2 = streamlit.columns([1, 1], vertical_alignment="bottom")
        c3, c4, c5 = c2.columns([1, 1, 1], vertical_alignment="bottom")
        
        exercise.name = c1.selectbox(
            "Exercise", options=global_exercise_names,
            index=global_exercise_names.index(exercise.name) if exercise.name in global_exercise_names else 0,
            key=f"c_name_{i}", label_visibility="collapsed"
        )
        exercise.sets = c3.number_input(
            "Sets", min_value=1, value=exercise.sets, key=f"c_sets_{i}", label_visibility="collapsed"
        )
        exercise.reps = c4.number_input(
            "Reps", min_value=1, value=exercise.reps, key=f"c_reps_{i}", label_visibility="collapsed"
        )
        exercise.remove = c5.checkbox(
            "Remove", value=exercise.remove, key=f"c_rem_{i}", label_visibility="collapsed"
        )

    # Actions
    col_add, col_del, col_save = streamlit.columns(3)

    if col_add.form_submit_button("Add", icon=":material/add:", use_container_width=True):
        # Method call instead of manual append
        routine.add_exercise(default_name=global_exercise_names[0])
        streamlit.rerun()

    if col_del.form_submit_button("Remove", icon=":material/delete:", use_container_width=True):
        # Method call instead of list comprehension
        routine.remove_flagged()
        streamlit.rerun()

    if col_save.form_submit_button("Save", icon=":material/save:", use_container_width=True):
        if not routine.name:
            streamlit.error("Routine name is required.")
        elif not routine.exercises:
            streamlit.error("Add at least one exercise.")
        else:
            # Conversion logic
            names = [ex.name for ex in routine.exercises]
            ids = getExerciseIDs(names)
            new_exercises = [
                RoutineExercise(
                    exercise_id=ids[idx], name=ex.name, 
                    target_sets=ex.sets, target_reps=ex.reps
                ) for idx, ex in enumerate(routine.exercises)
            ]
            
            new_routine = FullRoutine(
                id="", user_id=user_data.id, name=routine.name, exercises=new_exercises
            )

            if createUserRoutine(user_data, new_routine):
                streamlit.success("Routine Created!")
                state.clear_keys([state.KEY_ROUTINE_CREATOR])
                streamlit.switch_page("pages/routine/manager.py")
            else:
                streamlit.error("Creation failed.")

streamlit.divider()
if streamlit.button("Clear All", type="secondary"):
    state.clear_keys([state.KEY_ROUTINE_CREATOR])
    streamlit.rerun()