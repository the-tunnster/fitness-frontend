import streamlit

from database.read import getUser

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import User


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.title("Cardio Recorder", anchor=False)
streamlit.write("Select a cardio exercise to get started.")

user_data: User
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

streamlit.info("Sorry guys, gotta re-write this part. Should be out soon.")