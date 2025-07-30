import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", ])

streamlit.title("Post Workout Analytics", anchor=False)

user_data: User
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

if user_data.clearanceLevel < 1:
    streamlit.switch_page("home.py")

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

selected_routine_data: Routine = user_routines[user_routine_names.index(selected_routine_name) - 1 ]

data = getWorkoutComparison(user_data.id, selected_routine_data.id)

if data is None:
    streamlit.info("There aren't enough workouts saved for a comparison.")
    streamlit.stop()

for entry in data:
    streamlit.subheader(f"{entry["exercise_name"]}, {entry["variation"]}", anchor=False)
    col1, col2, col3 = streamlit.columns(3)
    col1.metric(label="Max Weight", value=entry["max_weight"], delta=None if entry['weight_change'] == 0 else f"{entry['weight_change']:.2f}")
    col2.metric(label="Total Reps", value=entry["reps"], delta=None if entry['reps_change'] == 0 else f"{entry['reps_change']:.2f}")
    col3.metric(label="Volume Moved", value=entry["volume"], delta=None if entry['volume_change'] == 0 else f"{entry['volume_change']:.2f}")