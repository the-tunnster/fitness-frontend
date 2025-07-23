import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", ])

streamlit.header("Post Workout Analytics", anchor=False)

user_data: User | None

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data is not None:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded.")
        streamlit.stop()
else:
    user_data = streamlit.session_state["user_data"]

if user_data is None:
    streamlit.stop()

streamlit.write("Select a workout routine to get started.")

user_routines = getRoutinesList(user_data.id)
if user_routines is None or user_routines == []:
    streamlit.info("You don't seem to have any routines set up. Please create one to access it here.")
    streamlit.stop()

user_routine_names: list[str] = ["None"] + [routine.name for routine in user_routines]

selected_routine_name: str = streamlit.selectbox(
    label="Select a routine",
    options=user_routine_names,
    index=0,
    key="start_routine_select",
    label_visibility="collapsed"
)

if selected_routine_name == "None":
    streamlit.stop()

selected_routine_data: Routine = user_routines[user_routine_names.index(selected_routine_name)]

data = getWorkoutComparison(user_data.id, selected_routine_data.id)

if data is None:
    streamlit.info("There aren't enough workouts saved for a comparison.")
    streamlit.stop()

for entry in data:
    streamlit.subheader(f"{entry["exercise_name"]}, {entry["variation"]}", anchor=False)
    col1, col2, col3 = streamlit.columns(3)
    col1.metric(label="Weight Lifted", value=entry["max_weight"], delta=f"{entry['max_weight']:.2f}")
    col2.metric(label="Reps Completed", value=entry["reps"], delta=f"{entry['reps_change']:.2f}")
    col3.metric(label="Volume Moved", value=entry["volume"], delta=f"{entry['volume_change']:.2f}")