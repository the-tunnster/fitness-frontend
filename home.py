import streamlit

from database.read import getUser
from database.create import createDummyUserProfile

from helpers.cache_manager import *
from helpers.user_interface import *


uiSetup()
initSessionState(["user_data"])

if not streamlit.user.is_logged_in:
    streamlit.header("Welcome.", anchor=False)
    streamlit.warning("You'll need to log in to continue")
    streamlit.stop()

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))

    if user_data is None:
        streamlit.info("This is your first time logging in.")
        result = createDummyUserProfile(str(streamlit.user.email), str(streamlit.user.given_name))

        if result:
            user_data = getUser(str(streamlit.user.email))
            streamlit.session_state["user_data"] = user_data
            streamlit.info("A dummy profile has been created. Feel free to update the information as you see fit.")

        else:
            streamlit.error("Couldn't create a new user")
            streamlit.stop()

    else:
        streamlit.session_state["user_data"] = user_data

streamlit.header(f"Welcome, {streamlit.session_state['user_data'].username}!", anchor=False)
streamlit.write("Your fitness journey starts here. This app is your companion to track, manage, and analyze your workouts.")

streamlit.subheader("Features at a Glance", anchor=False)
streamlit.markdown("""
- 🏋️ **Workout Recorder**: Log your cardio and strength workouts effortlessly.
- 📋 **Routine Manager**: Create and customize your personal workout routines.
- 📊 **Analytics**: Gain insights with detailed workout analytics.
- 👤 **User Profile**: Manage your personal information with ease.
""")

streamlit.subheader("Getting Started and Need Help?", anchor=False)
with streamlit.expander("Routine Creation"):
    streamlit.write("""
    - To add an exercise, select a high-level option. Variations and equipment can be chosen during the workout.
    - To remove exercises, use the checkboxes and click "Remove". Ensure you've saved changes before leaving the page.
    """)

with streamlit.expander("Workout Tips"):
    streamlit.write("""
    - The first workout may show "Exercise Name (None, None)". Select your equipment and variation, and then "Update" to fix this.
    - Future workouts will remember your last settings for convenience.
    """)