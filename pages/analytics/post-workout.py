import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", ])

streamlit.header("Coming Soon...", anchor=False)