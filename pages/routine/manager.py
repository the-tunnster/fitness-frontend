import streamlit
from typing import Any

from models.user import BasicUser
from models.routines import RoutineExercise, FullRoutine

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import getBasicUser, getExerciseList, getExerciseIDs, getRoutinesList, getRoutineData
from database.update import updateUserRoutine
from database.delete import deleteRoutine


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", "routine_editor_data"])

streamlit.title("Routine Management", anchor=False)
streamlit.write("""This is where you'll manage existing routines and their set-ups.<br>
Select a routine to get started.<br>
""", unsafe_allow_html=True)

user_data: BasicUser
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getBasicUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

if user_data.clearance_level < 1:
    accessControlWarning()
    getInTouch()
    streamlit.stop()

if streamlit.session_state["routine_editor_data"] is None:
    streamlit.session_state["routine_editor_data"] = {"exercises": [], "name": "None"}
routine_editor_data = streamlit.session_state["routine_editor_data"]

routine_editor_exercises: list[dict[str, Any]] = streamlit.session_state["routine_editor_data"]["exercises"]

global_exercise_names: list[str] | None = None
global_exercise_list = getExerciseList()

if global_exercise_list is not None:
    global_exercise_names = [exercise.name for exercise in global_exercise_list]
else:
    global_exercise_list = []
    global_exercise_names = []

user_routines_list = getRoutinesList(user_id=user_data.id)
if user_routines_list is None or user_routines_list == []:
    streamlit.info("You don't seem to have any routines set up. Please create one to access it here.")
    streamlit.stop()
    
user_routine_names = ["None"] + [routine.name for routine in user_routines_list]

selected_routine_name = streamlit.selectbox(
    label="Select a routine",
    options=user_routine_names,
    index=0,
    label_visibility="collapsed"
)

if selected_routine_name == "None":
    streamlit.session_state["routine_editor_data"] = {"exercises": [], "name": "None"}
    routine_editor_exercises = streamlit.session_state["routine_editor_data"]["exercises"]
    streamlit.stop()

if streamlit.session_state["routine_editor_data"]["name"] != selected_routine_name:
    streamlit.session_state["routine_editor_data"] = {"exercises": [], "name": selected_routine_name}
    routine_editor_exercises = streamlit.session_state["routine_editor_data"]["exercises"]

selected_routine_index = user_routine_names.index(selected_routine_name)
selected_routine = user_routines_list[selected_routine_index - 1]

full_user_routine = getRoutineData(user_data.id, selected_routine.id)
if full_user_routine is None:
    streamlit.error("Failed to load routine data. Please try again.")
    streamlit.session_state["routine_editor_data"] = {"exercises": [], "name": selected_routine_name}
    routine_editor_exercises = streamlit.session_state["routine_editor_data"]["exercises"]
    streamlit.stop()

if not routine_editor_exercises :
    for ex in full_user_routine.exercises:
        routine_editor_exercises.append({
            "name": ex.name,
            "sets": ex.target_sets,
            "reps": ex.target_reps,
            "remove": False,
        })
    streamlit.session_state["routine_editor_data"]["exercises"] = routine_editor_exercises

streamlit.caption("☑️ Select exercises to delete, then press '🗑️ Delete Selected' to remove them.")
streamlit.divider()

with streamlit.form("routine_viewer", clear_on_submit=False, border=False, enter_to_submit=False):
    for i, exercise in enumerate(routine_editor_exercises):
        col1, col2 = streamlit.columns([1, 1], vertical_alignment="bottom")
        col3, col4, col5 = col2.columns([1, 1, 1], vertical_alignment="bottom")

        if i == 0:
            col1.write("Exercise Name")
            col3.write("Sets")
            col4.write("Reps")

        exercise["name"] = col1.selectbox(
            "Exercise", options=global_exercise_names,
            index=global_exercise_names.index(exercise["name"]) if exercise["name"] in global_exercise_names else 0,
            key=f"name_{i}", label_visibility="collapsed"
        )

        exercise["sets"] = col3.number_input(
            "Sets", min_value=1, value=exercise["sets"], step=1,
            key=f"sets_{i}", label_visibility="collapsed"
        )

        exercise["reps"] = col4.number_input(
            "Reps", min_value=1, value=exercise["reps"], step=1,
            key=f"reps_{i}", label_visibility="collapsed"
        )

        exercise["remove"] = col5.checkbox(
            "Remove", value=exercise.get("remove", False),
            key=f"remove_{i}", label_visibility="collapsed"
        )

    streamlit.divider()
    col_add, col_delete, col_save = streamlit.columns([1, 1, 1])

    if col_add.form_submit_button("Add", icon=":material/add:", use_container_width=True):
        routine_editor_exercises.append({
            "name": global_exercise_names[0],
            "sets": 3,
            "reps": 10,
            "remove": False,
        })
        streamlit.rerun()

    if col_delete.form_submit_button("Remove", icon=":material/delete:", use_container_width=True):
        routine_editor_data["exercises"] = [ex for ex in routine_editor_exercises if not ex.get("remove", False)]
        streamlit.rerun()

    if col_save.form_submit_button("Save", icon=":material/save:", use_container_width=True):

        names = [ex["name"] for ex in routine_editor_data["exercises"]]
        ids = getExerciseIDs(names)

        updated_exercises: list[RoutineExercise] = []

        for idx, ex in enumerate(routine_editor_data["exercises"]):
            updated_exercises.append(
                RoutineExercise(
                    exercise_id=ids[idx],
                    name=ex["name"],
                    target_sets=ex["sets"],
                    target_reps=ex["reps"]
                )
            )

        updated_routine = FullRoutine(
            id=full_user_routine.id,
            user_id=user_data.id,                                                                                         #type: ignore
            name=full_user_routine.name,
            exercises=updated_exercises,
        )

        result = updateUserRoutine(user_data, updated_routine)
        if result:
            streamlit.success("Routine saved!")
            del streamlit.session_state["routine_editor_data"], routine_editor_data, routine_editor_exercises
        else:
            streamlit.error("That didn't work.")

with streamlit.expander("Delete This Routine", expanded=False, icon=":material/delete:"):
    streamlit.warning("This action is technically reversible, but it is a hassle to re-create a whole new routine.")

    confirm_delete = streamlit.checkbox("I understand and want to delete this routine")

    if confirm_delete:
        if streamlit.button("Delete Routine", type="primary"):
            result = deleteRoutine(user_data.id, selected_routine.id)

            if result:
                streamlit.success("Deleted Routine")
                clearSessionVariable(["routine_editor_data"])
                routine_editor_data, routine_editor_exercises = [], []
                streamlit.rerun()
            else:
                streamlit.error("That didn't work.")