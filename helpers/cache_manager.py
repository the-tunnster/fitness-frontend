import streamlit 
from typing import List

def initSessionState(keys: List[str] = []):
	if keys == []:
		keys = [
			"user_data",
			"routine_creator_data", "routine_editor_data", 
			"workout_session_data", "current_exercise_index", "add_exercise_dialog",
			"workout_exercise_selection"
		]
	
	for key in keys:
		if key not in streamlit.session_state:
			streamlit.session_state[key] = None


def clearSessionVariable(keys: List[str]):
	for key in keys:
		if key in streamlit.session_state:
			del streamlit.session_state[key]