import streamlit                                                                     # type:ignore

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import BasicUser
from database.read import getBasicUser


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", "strava_code"])

streamlit.title("Cardio History", anchor=False)

user_data: BasicUser
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getBasicUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

streamlit.info("Sorry guys, gotta re-write this part. Should be out soon.")