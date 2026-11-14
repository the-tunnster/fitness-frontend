import streamlit

from database.read import getBasicUser

from helpers.state_manager import AppState
from helpers.user_interface import *


uiSetup()
state = AppState()

if state.user is None:
    state.user = getBasicUser()
    if state.user is None:
        streamlit.error("Couldn't reach the backend.")
        streamlit.stop()

user_data = state.user

streamlit.title(f"Welcome, {user_data.username}!", anchor=False)

streamlit.markdown("""
The app is in early development. Some things may be broken, and some might be confusing. <br>
For now though, jump right in! <br>
""", unsafe_allow_html=True)

streamlit.page_link(page="pages/strength-training/workout.py", label="Record a Session", icon=":material/exercise:", use_container_width=True)
streamlit.page_link(page="pages/user/profile.py", label="Account Management", icon=":material/account_box:", use_container_width=True)