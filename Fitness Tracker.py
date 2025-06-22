import streamlit

from database.read import *
from database.create import *

from helpers.cache_manager import *
from helpers.user_interface import *

streamlit.set_page_config(
    page_title="Workout Tracker",
    page_icon="🏋️",
    layout="wide",
)

uiSetup()
initSessionState()

streamlit.header("Welcome to the Workout Tracker")

if not streamlit.user.is_logged_in:
    streamlit.warning("You'll need to sign in to continue")
    streamlit.stop()

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))

    if user_data is None:
        streamlit.info("This is your first time logging in.")
        userID = createDummyUserProfile(str(streamlit.user.email), str(streamlit.user.given_name))

        if userID is not None:
            user_data = getUser(str(streamlit.user.email))
            streamlit.info("A dummy profile has ben created.")

        else:
            streamlit.error("Couldn't create a new user")

    else:
        streamlit.session_state["user_data"] = user_data

streamlit.info("Welcome " + streamlit.session_state["user_data"].username + ".")

if not streamlit.session_state["popup_seen"]:
    popUpInfo()

streamlit.markdown("""
                   
Congratulations on making it this far. </br>
I was sure something would've broken by now. </br>
But here we are. </br>
                   
In any case, let's get started. </br>
The sidebar navigation should help you get around. </br>
If you come across any issues, please let me know, and I'll get onto fixing it ASAP. </br>
For now though, it is in super early development, so please try and break it?. </br>

Good luck, and have a G lift! </br>

""", unsafe_allow_html=True)