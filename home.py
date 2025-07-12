import streamlit

from database.read import *
from database.create import *

from helpers.cache_manager import *
from helpers.user_interface import *

streamlit.set_page_config(
    page_title="Home Page",
    page_icon="💪🏻",
    layout="wide",
    initial_sidebar_state="expanded"
)

uiSetup()
initSessionState()

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

streamlit.header("Welcome " + streamlit.session_state["user_data"].username + "!", anchor=False)

streamlit.write("This application is designed to help you track your fitness journey, manage routines, record workouts, and analyze progress.")

streamlit.subheader("Features Overview", anchor=False)
streamlit.write("""
- **Workout Recorder**: Log your cardio and strength workouts.
- **Routine Manager**: Create and manage your personal routines.
- **Analytics**: Dive into your workout data with historic and post-workout analytics.
- **User Profile**: Update and manage your personal information.

Feel free to explore and make the most of the features, and I'll be adding new ones as I go.
In the meantime, if you encounter any issues or think of any cool new features you want, let me know and I'll get on it.
Good luck, and enjoy your fitness journey!
                """)