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

user_data = streamlit.session_state["user_data"]

streamlit.header(f"Welcome, {streamlit.session_state['user_data'].username}!", anchor=False)

if user_data.clearanceLevel < 1:
    streamlit.write("""
    I've decided to restrict usage to those who actually seem like they'd benefit from this app. <br>
    Some of ya'll are just not worth developing for, and I'd much rather focus on the others. <br>
    If you want access, gimme a call or send me a DM and I'll approve your access personally. <br>
    """, unsafe_allow_html=True)
    col1, col2 = streamlit.columns([1, 1])
    col1.link_button(label="Instagram DM", url="https://www.instagram.com/the_tunnster/", icon=":material/chat:")
    col2.link_button(label="Call", url="tel:+61493648088", icon=":material/add_call:")
    streamlit.stop()

streamlit.write("""
The app is in early development. Some things may be broken, and some might be confusing.
If you need help, there is a small section below. If that doesn't help, just gimme a call or reach out.""")

streamlit.divider()

streamlit.subheader("Features", anchor=False)
with streamlit.expander("Current"):
    streamlit.markdown("""
    - **Routine Manager**: <br> Create and customize your personal workout routines. This is essential to the next feature.
    - **Workout Recorder**: <br> Log your cardio and strength workouts effortlessly. Literally depends on you having set up routines.
    - **Analytics**: <br> Gain insights with analytics. If you're a bit lost, I'd be happy to explain, below.
    - **User Profile**: <br> Manage your personal information with ease.
    """, unsafe_allow_html=True)

with streamlit.expander("Upcoming"):
    streamlit.markdown("""
    - **Freestyle Mode**: <br> Annoyed by the fact that you need a routine to workout? You don't have to be. Soon.
    - **Exercise Modifier**: <br> Since some of y'all have non-standard exercise variaitons or equipment, I'll set up something cleaner. However, there is obviously room for abuse here, so it'll take a bit longer.
    - **Leaderboards**: <br> A large aspect of hitting the gym is having someone to out-lift or compete with. I'll be adding "Leaderboard Routines" that you can do to see how you stack up against the rest of the users. Some ML will go into this, so its normalised.
    - **Predictive Lifting/Growth**: <br> Since I re-wrote everything, the ML stuff from before has to be re-designed as well. This also needs user data for me to train on, so please use this as mch as possible.
    - **Muscle Group Balancing**: <br> Using analytics, I'm hoping I can help you identify what groups you're under-training and suggest supplemets to your workouts.
    """, unsafe_allow_html=True)

streamlit.divider()

streamlit.subheader("Getting Started and Need Help?", anchor=False)
with streamlit.expander("Routines"):
    streamlit.write("""
    - To add an exercise, select a high-level option. Variations and equipment can be chosen during the workout.
    - To remove exercises, use the checkboxes and click "Remove". Ensure you've saved changes before leaving the page.
    """)

with streamlit.expander("Workouts"):
    streamlit.write("""
    - The first workout may show "Exercise Name (None, None)". Select your equipment and variation, and then "Update" to fix this.
    - Future workouts will remember your last settings for convenience.
    """)

with streamlit.expander("Analytics"):
    streamlit.write("""
    - The charts are comparisons of volume moved (weight X reps) and maximum weight lifted in a session.
    - You can see the variance between the two over time, and figure out your rhythym for future workouts.
    """)