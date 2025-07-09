import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *

streamlit.set_page_config(
    page_title="Post Workout Analysis",
    page_icon=":material/table_chart_view:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("./Fitness Tracker.py")

uiSetup()
initSessionState()

streamlit.header("Workout Analytics", anchor=False)

user_data: User | None

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data is not None:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded. Please log in again.")
        streamlit.stop()
else:
    user_data = streamlit.session_state["user_data"]

