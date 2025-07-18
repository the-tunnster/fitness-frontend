import streamlit

from models.user import User

from database.read import getUser
from database.update import updateUserProfile

from helpers.cache_manager import *
from helpers.user_interface import *


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.header("Profile Management.", anchor=False)
streamlit.markdown("""
This is your user profile page. </br>
Feel free to leave these values as they are, I chose dummy values. </br>
However, if you wish to update these, try to have them as accurate as possible. </br>
""", unsafe_allow_html=True)

user_data: User

if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))

user_data = streamlit.session_state["user_data"]

with streamlit.form("user_profile", enter_to_submit=False):
    gender_index = 0 if user_data.gender == "male" else 1
    user_data.dateOfBirth = str(user_data.dateOfBirth)
    unit_preference_index = 0 if user_data.unitPreference == "metric" else 1

    user_name = streamlit.text_input(label="user_name", value=user_data.username)
    email_id = streamlit.text_input(label="email_id", value=user_data.email, disabled=True)
    gender = streamlit.selectbox(label="gender", options=["male", "female"], index=gender_index)
    date_of_birth = streamlit.date_input(label="date_of_birth", value=user_data.dateOfBirth)
    height = streamlit.number_input(label="height", value=user_data.height)
    weight = streamlit.number_input(label="weight", value=user_data.weight)
    unit_preference = streamlit.selectbox(label="unit_preference", options=["metric", "freedom"], index=unit_preference_index)
    id = streamlit.text_input(label="user_id", value=user_data.id, disabled=True)

    submitted = streamlit.form_submit_button("Update Information")
    if submitted:
        updated_user = User(
            username=str(user_name),
            email=str(email_id),
            gender=gender,
            dateOfBirth=date_of_birth.isoformat(),
            height=height,
            weight=weight,
            unitPreference=unit_preference,
            id=None
        )
        result = updateUserProfile(updated_user, user_data.id) # type: ignore
        if result == True:
            streamlit.success("Updated user profile!")
            streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
        else:
            streamlit.error("Couldn't update profile...")
