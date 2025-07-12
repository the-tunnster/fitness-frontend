import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

streamlit.set_page_config(
    page_title="Cardiovascular",
    page_icon=":material/sprint:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.header("Coming Soon...", anchor=False)