import time
import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *
from database.create import *

streamlit.set_page_config(
    page_title="Routine Creator",
    page_icon=":material/add_notes:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("./Fitness Tracker.py")

uiSetup()
initSessionState()

user_data: User

if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))

if streamlit.session_state["routine_creator_data"] is None:
    streamlit.session_state["routine_creator_data"] = {
        "exercises": [],
        "name": "",
        "description": ""
    }

user_data = streamlit.session_state["user_data"]
routine_creator_data = streamlit.session_state["routine_creator_data"]
routine_creator_exercises = routine_creator_data["exercises"]

streamlit.header("Create a New Routine.", anchor=False)

streamlit.markdown(""" Add a routine name and build your workout from scratch. """, unsafe_allow_html=True)

# Input fields for routine name and description
routine_creator_data["name"] = streamlit.text_input("Routine Name", value=routine_creator_data.get("name", ""))

streamlit.divider()

global_exercise_names: list[str] | None = None
global_exercise_list = getExerciseList()

if global_exercise_list is not None:
    global_exercise_names = [exercise.name for exercise in global_exercise_list]
else:
    global_exercise_list = []
    global_exercise_names = []

streamlit.caption("☑️ Tick exercises to delete, then press '🗑️ Delete Selected'")
streamlit.divider()

with streamlit.form("routine_creator_form", clear_on_submit=False, border=False):
    for i, exercise in enumerate(routine_creator_exercises):
        col1, col2 = streamlit.columns([1, 1], vertical_alignment="bottom")
        col3, col4, col5 = col2.columns([1, 1, 1], vertical_alignment="bottom")

        if i == 0:
            col1.write("Exercise Name")
            col3.write("Sets")
            col4.write("Reps")

        exercise["name"] = col1.selectbox(
            label="Exercise", options=global_exercise_names,
            index=global_exercise_names.index(exercise["name"]) if exercise["name"] in global_exercise_names else 0,
            key=f"name_creator_{i}", label_visibility="collapsed"
        )

        exercise["sets"] = col3.number_input(
            "Sets", min_value=1, value=exercise["sets"], step=1,
            key=f"sets_creator_{i}", label_visibility="collapsed"
        )

        exercise["reps"] = col4.number_input(
            "Reps", min_value=1, value=exercise["reps"], step=1,
            key=f"reps_creator_{i}", label_visibility="collapsed"
        )

        exercise["remove"] = col5.checkbox(
            "Remove", value=exercise.get("remove", False),
            key=f"remove_creator_{i}", label_visibility="collapsed"
        )

    streamlit.divider()
    col_add, col_delete, col_save = streamlit.columns([1, 1, 1])

    if col_add.form_submit_button("Add", icon=":material/add:", use_container_width=True):
        routine_creator_exercises.append({
            "name": global_exercise_names[0],
            "sets": 3,
            "reps": 10,
            "remove": False,
        })
        streamlit.rerun()

    if col_delete.form_submit_button("Remove", icon=":material/delete:", use_container_width=True):
        routine_creator_data["exercises"] = [ex for ex in routine_creator_exercises if not ex.get("remove", False)]
        streamlit.rerun()

    if col_save.form_submit_button("Save", icon=":material/save:", use_container_width=True):
        if not routine_creator_data["name"]:
            streamlit.error("Routine name is required.")
        elif len(routine_creator_data["exercises"]) == 0:
            streamlit.error("Please add at least one exercise.")
        else:
            names = [ex["name"] for ex in routine_creator_data["exercises"]]
            ids = getExerciseIDs(names)

            new_exercises: List[RoutineExercise] = []

            for idx, ex in enumerate(routine_creator_data["exercises"]):
                new_exercises.append(
                    RoutineExercise(
                        exercise_id=ids[idx],
                        name=ex["name"],
                        target_sets=ex["sets"],
                        target_reps=ex["reps"]
                    )
                )

            new_routine = FullRoutine(
                id="",
                user_id=user_data.id, #type: ignore
                name=routine_creator_data["name"],
                exercises=new_exercises
            )

            result = createUserRoutine(user_data, new_routine)
            if result:
                streamlit.success("Routine created successfully!")
                del streamlit.session_state["routine_creator_data"]
                time.sleep(3)
                streamlit.rerun()
            else:
                streamlit.error("That didn't work.")

streamlit.markdown("---")

if streamlit.button("Clear All", type="secondary"):
    del streamlit.session_state["routine_creator_data"]
    streamlit.rerun()
