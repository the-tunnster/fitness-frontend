import streamlit
import requests

from helpers.cache_manager import *
from helpers.user_interface import *

from config.strava_urls import *

from database.read import getFullUser
from database.update import updateUserProfile

from models.user import FullUser

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])


streamlit.title("Strava Auth Verification", anchor=False)

streamlit.write("This is a work in progress. Come back later.")
streamlit.stop()

user_data: FullUser | None = getFullUser(str(streamlit.user.email))
if user_data is None:
    streamlit.stop()

if "code" in streamlit.query_params:
    response = requests.post(url=TOKEN_GRANT_URL+f"&code={streamlit.query_params["code"]}")

    if response.status_code != 200:
        streamlit.error("There was an issue with authetication. Please try again later.")
        streamlit.stop()
    
    response_data = response.json()
    user_data.stravaRefreshToken = response_data["refresh_token"]
    user_data.stravaAccessToken = response_data["access_token"]

    result = updateUserProfile(user_data, user_data.id)
    if result == True:
        streamlit.success("Updated user profile with strava auth tokens")
        streamlit.cache_data.clear()
        streamlit.session_state["user_data"] = getFullUser(str(streamlit.user.email))
        streamlit.info("You can close this page now!")
        streamlit.stop()
    else:
        streamlit.error("Couldn't update profile...")
        streamlit.stop()