import streamlit

from database.read import getExerciseList, getBasicUser

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import BasicUser


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.title("Exercise Viewer", anchor=False)
streamlit.write("Select an exercise to view it's variations and equipment options.")

user_data: BasicUser
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getBasicUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]


if user_data.clearanceLevel < 1:
    accessControlWarning()
    getInTouch()
    streamlit.stop()
    
global_exercise_names: list[str] | None = None
global_exercise_list = getExerciseList()

if global_exercise_list is not None:
	global_exercise_names = [exercise.name for exercise in global_exercise_list]
else:
	global_exercise_list = []
	global_exercise_names = []


selected_exercise_name = streamlit.selectbox(
	label="Select a new exercise to add",
	options=["None"] + global_exercise_names,
    label_visibility="collapsed"
    )

if selected_exercise_name == "None":
    streamlit.stop()

selected_exercise_data = global_exercise_list[global_exercise_names.index(selected_exercise_name)]

streamlit.divider()

col1, col2 = streamlit.columns([1, 1])
col1.write("Available Variations:")
for i in selected_exercise_data.variations:
    col2.write(i)
     
streamlit.divider()

col1, col2 = streamlit.columns([1, 1])
col1.write("Available Equipment:")
for i in selected_exercise_data.equipment:
    col2.write(i)