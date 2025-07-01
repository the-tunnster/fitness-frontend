import streamlit 
from typing import List

def initSessionState(keys: List[str] = []):
	if keys is []:
		keys = [
			"popup_seen",
			"user_data",
			"routine_creator_data", "routine_editor_data", 
			"workout_session_data", "workout_status"
		]
	
	for key in keys:
		if key not in streamlit.session_state:
			streamlit.session_state[key] = None


def clearSessionVariable(variable_name: str):
	if variable_name in streamlit.session_state:
		del streamlit.session_state[variable_name]