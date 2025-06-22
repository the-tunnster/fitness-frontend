import streamlit 

def initSessionState():
	if "user_data" not in streamlit.session_state:
		streamlit.session_state["user_data"] = None

	if "popup_seen" not in streamlit.session_state:
		streamlit.session_state["popup_seen"] = False

	if "routine_editor_data" not in streamlit.session_state:
		streamlit.session_state["routine_editor_data"] = None

	if "routine_creator_data" not in streamlit.session_state:
		streamlit.session_state["routine_creator_data"] = None
	
	if "workout_session_data" not in streamlit.session_state:
		streamlit.session_state["workout_session_data"] = None