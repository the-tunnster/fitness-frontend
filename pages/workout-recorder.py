import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *

streamlit.set_page_config(
    page_title="Routine Creator",
    page_icon=":material/add_notes:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("./Fitness Tracker.py")

uiSetup()
initSessionState()

if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))

if streamlit.session_state["workout_session_data"] is None:
    if getWorkoutSessionData(str(streamlit.user.email)) is None:
        streamlit.session_state["workout_session_data"] = {}
    else:
        streamlit.session_state["workout_session_data"] = getWorkoutSessionData(str(streamlit.user.email))

user_data = streamlit.session_state["user_data"]
workout_session_data = streamlit.session_state["workout_session_data"]

streamlit.markdown("""
                   # Workout.</br>
                   """, unsafe_allow_html=True)

user_routines_list = getRoutinesList(user_id=user_data.id)
if user_routines_list is None:
    streamlit.info("You don't seem to have any routines set up. Please create one to access it here.")
    streamlit.stop()
    
user_routine_names = [routine.name for routine in user_routines_list]

selected_routine_name = streamlit.selectbox("Select a routine", options=user_routine_names, index=0)
selected_routine_index = user_routine_names.index(selected_routine_name)
selected_routine = user_routines_list[selected_routine_index]

if workout_session_data == {}:
    start_workout = streamlit.button("Start Workout")
else:
    start_workout = True

if not start_workout:
    streamlit.stop()

workout_session_data = createWorkoutSession(user_data.id, selected_routine.id)