import streamlit

from database.read import getBasicUser
from database.create import createDummyUserProfile

from helpers.cache_manager import *
from helpers.user_interface import *


uiSetup()
initSessionState(["user_data"])

if not streamlit.user.is_logged_in:
    streamlit.title("Welcome.", anchor=False)
    streamlit.warning("You'll need to log in to continue. (It's in the sidebar)")
    streamlit.stop()

if streamlit.session_state["user_data"] is None:
    user_data = getBasicUser(str(streamlit.user.email))

    if user_data is None:
        streamlit.info("This is your first time logging in.")
        result = createDummyUserProfile(str(streamlit.user.email), str(streamlit.user.given_name))

        if result:
            streamlit.cache_data.clear()
            user_data = getBasicUser(str(streamlit.user.email))
            streamlit.session_state["user_data"] = user_data
            streamlit.info("A dummy profile has been created. Feel free to update the information as you see fit.")

        else:
            streamlit.error("Couldn't create a new user")
            streamlit.stop()

    else:
        streamlit.session_state["user_data"] = user_data

user_data = streamlit.session_state["user_data"]

streamlit.title(f"Welcome, {user_data.username}!", anchor=False)

if user_data.clearance_level < 1:
    accessControlWarning()
    getInTouch()
    streamlit.stop()

streamlit.markdown("""
The app is in early development. Some things may be broken, and some might be confusing. <br>
For now though, jump right in! <br>
""", unsafe_allow_html=True)

streamlit.page_link(page="pages/strength-training/workout.py", label="Record a Session", icon=":material/exercise:", use_container_width=True)
streamlit.page_link(page="pages/user/profile.py", label="Account Management", icon=":material/account_box:", use_container_width=True)