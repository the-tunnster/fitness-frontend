import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *
from database.create import *

streamlit.set_page_config(
    page_title="Analytics",
    page_icon=":material/table_chart_view:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("./Fitness Tracker.py")

uiSetup()
initSessionState()

user_data: User

if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]
    
streamlit.header("Analytics")

streamlit.write("Work in progress type shii")
streamlit.write("May take a week or so, my bad g")

# Check analytics collection for consolidated workout history
# 	If yes --> fetch all exercise data
# 	If no  --> build analytics document

# Check analytics document for exercises and histories

# Display metrics (?)