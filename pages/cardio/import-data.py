import streamlit

from database.read import getFullUser

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import FullUser

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.title("Import Cardio Data", anchor=False)

streamlit.write("This is a work in progress. Come back later.")
streamlit.stop()

user_data: FullUser | None = getFullUser(str(streamlit.user.email))
if user_data is None:
    streamlit.stop()

if user_data.stravaAccessToken == "":
    streamlit.markdown("""You'll need to authenticate with Strava before continuing. <br>
                       Please click on the button below. <br>""", unsafe_allow_html=True)
    
    streamlit.link_button(label="Authenticate", url=AUTH_URL)
    streamlit.stop()

