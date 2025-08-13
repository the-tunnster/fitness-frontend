import streamlit                                                                     # type:ignore

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", "strava_code"])

streamlit.title("Cardio History", anchor=False)

user_data: User
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

streamlit.info("Sorry guys, gotta re-write this part. Should be out soon.")