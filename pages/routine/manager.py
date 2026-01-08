import streamlit
from helpers.state_manager import AppState, BuilderExercise
from helpers.user_interface import *
from database.read import getBasicUser, getExerciseList, getExerciseIDs, getRoutinesList, getRoutineData
from database.update import updateUserRoutine
from database.delete import deleteRoutine
from models.routines import RoutineExercise, FullRoutine

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
state = AppState()
streamlit.title("Routine Management", anchor=False)

# --- Auth ---
if state.user is None:
    state.user = getBasicUser(str(streamlit.user.email))
if state.user is None or state.user.clearance_level < 1:
    accessControlWarning()
    streamlit.stop()
user_data = state.user

# --- Load State (Rich Object) ---
routine_editor = state.get_or_create_routine_editor()

# --- Routine Selection Logic ---
user_routines = getRoutinesList(user_id=user_data.id) or []
if not user_routines:
    streamlit.info("No routines found.")
    streamlit.stop()

routine_names = ["None"] + [r.name for r in user_routines]
selected_name = streamlit.selectbox("Select Routine", options=routine_names)

# Reset state if selection changes
if selected_name == "None":
    if routine_editor.name != "None":
        state.clear_keys([state.KEY_ROUTINE_EDITOR])
    streamlit.stop()

if routine_editor.name != selected_name:
    # Load new routine from DB into State Object
    routine_editor.clear() # Reset
    routine_editor.name = selected_name
    
    # Find ID and fetch full data
    r_index = routine_names.index(selected_name)
    r_id = user_routines[r_index - 1].id
    full_data = getRoutineData(user_data.id, r_id)
    
    if full_data:
        # Map DB model to View Model
        for ex in full_data.exercises:
            routine_editor.exercises.append(
                BuilderExercise(name=ex.name, sets=ex.target_sets, reps=ex.target_reps)
            )
    else:
        streamlit.error("Could not load routine.")

# --- Editor Form ---
global_exercise_list = getExerciseList() or []
global_names = [ex.name for ex in global_exercise_list] or ["None"]

streamlit.caption("☑️ Select exercises to delete, then press 'Remove' to drop them.")
streamlit.divider()

with streamlit.form("routine_viewer", border=False, enter_to_submit=False):

    # Header
    h1, h2 = streamlit.columns([1, 1], vertical_alignment="bottom")
    h3, h4, h5 = h2.columns([1, 1, 1], vertical_alignment="bottom")
    h1.write("Exercise Name")
    h3.write("Sets")
    h4.write("Reps")


    for i, exercise in enumerate(routine_editor.exercises):
        c1, c2 = streamlit.columns([1, 1], vertical_alignment="bottom")
        c3, c4, c5 = c2.columns([1, 1, 1], vertical_alignment="bottom")
        
        exercise.name = c1.selectbox(
            "Exercise", options=global_names,
            index=global_names.index(exercise.name) if exercise.name in global_names else 0,
            key=f"e_name_{i}", label_visibility="collapsed"
        )
        exercise.sets = c3.number_input("Sets", min_value=1, value=exercise.sets, key=f"e_sets_{i}", label_visibility="collapsed")
        exercise.reps = c4.number_input("Reps", min_value=1, value=exercise.reps, key=f"e_reps_{i}", label_visibility="collapsed")
        exercise.remove = c5.checkbox("Remove", value=exercise.remove, key=f"e_rem_{i}", label_visibility="collapsed")
    
    streamlit.divider()
    c_add, c_del, c_save = streamlit.columns(3)
    
    if c_add.form_submit_button("Add", icon=":material/add:", use_container_width=True):
        routine_editor.add_exercise(default_name=global_names[0])
        streamlit.rerun()

    if c_del.form_submit_button("Remove", icon=":material/delete:", use_container_width=True):
        routine_editor.remove_flagged()
        streamlit.rerun()

    if c_save.form_submit_button("Save", icon=":material/save:", use_container_width=True):
        # Re-fetch ID
        r_index = routine_names.index(selected_name)
        r_id = user_routines[r_index - 1].id
        
        names = [ex.name for ex in routine_editor.exercises]
        ids = getExerciseIDs(names)
        
        updated_exercises = [
            RoutineExercise(exercise_id=ids[i], name=ex.name, target_sets=ex.sets, target_reps=ex.reps)
            for i, ex in enumerate(routine_editor.exercises)
        ]
        
        updated_routine = FullRoutine(id=r_id, user_id=user_data.id, name=routine_editor.name, exercises=updated_exercises)
        
        if updateUserRoutine(user_data, updated_routine):
            streamlit.success("Saved!")
            state.clear_keys([state.KEY_ROUTINE_EDITOR])
            streamlit.rerun()
        else:
            streamlit.error("Save failed.")

# --- Deletion Section ---
with streamlit.expander("Delete This Routine", expanded=False, icon=":material/delete:"):
    streamlit.warning("This action is technically reversible, but it is a hassle to re-create a whole new routine.")

    if streamlit.checkbox("I understand and want to delete this routine"):
        if streamlit.button("Delete Routine", type="primary"):
            # Fetch ID (must calculate again as it's outside the form scope)
            r_index = routine_names.index(selected_name)
            r_id = user_routines[r_index - 1].id
            
            if deleteRoutine(user_data.id, r_id):
                streamlit.success("Deleted Routine")
                # Clear the editor state so it doesn't try to load the deleted routine
                state.clear_keys([state.KEY_ROUTINE_EDITOR])
                streamlit.rerun()
            else:
                streamlit.error("That didn't work.")