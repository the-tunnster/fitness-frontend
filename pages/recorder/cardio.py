import streamlit

from database.read import getCardioList, getUser
from database.update import updateCardioHistory

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import User
from models.cardio import CardioMetric, CardioSession


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.header("Cardio Recorder", anchor=False)
streamlit.write("Select a cardio exercise to get started.")

user_data: User | None

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data is not None:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded.")
        streamlit.stop()
else:
    user_data = streamlit.session_state["user_data"]

if user_data is None:
    streamlit.stop()

cardio_list = getCardioList()
cardio_names: list[str]

if cardio_list is not None:
    cardio_names = ["None"] + [cardio.name for cardio in cardio_list]
else:
    streamlit.stop()

selected_cardio_name = streamlit.selectbox(
    label="Select cardio",
    options=cardio_names,
    label_visibility="collapsed",
)

if selected_cardio_name == "None":
    streamlit.stop()

selected_cardio_data = cardio_list[cardio_names.index(selected_cardio_name) - 1]

with streamlit.form("cardio_form", enter_to_submit=False):
    col1, col2 = streamlit.columns([1, 1])

    col1.write("Variation")
    col1.text('')
    variation = col2.selectbox("variation", options=selected_cardio_data.variations, label_visibility="collapsed")

    col1.write("Total Distance")
    col1.text('')
    total_distance = col2.number_input("Enter total distance (km)", min_value=0.0, step=0.1, label_visibility="collapsed")

    col1.write("Total Time")
    col1.text('')
    total_time = col2.number_input("Enter total time (minutes)", min_value=0.0, step=1.0, label_visibility="collapsed")

    col1.write("Calories Burned")
    col1.text('')
    calories_burned = col2.number_input("Enter calories burned", min_value=0, step=1, label_visibility="collapsed")

    col1.write("Heart Rate")
    col1.text('')
    heart_rate = col2.number_input("Enter heart rate (bpm)", min_value=0, step=1, label_visibility="collapsed")

    submitted = streamlit.form_submit_button("Save Session Data", use_container_width=True)

if submitted:
    cardio_session = CardioSession(
        variation=variation,
        metrics=CardioMetric(
            total_distance=total_distance,
            total_time=total_time,
            calories_burned=calories_burned,
            heart_rate=heart_rate,
        )
    )

    result = updateCardioHistory(user_data.id, selected_cardio_data.id, cardio_session)
    if result:
        streamlit.switch_page("pages/analytics/post-cardio.py")