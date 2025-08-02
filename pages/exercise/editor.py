import streamlit

from database.read import getExerciseList, getUser
from database.update import updateExercise

from helpers.cache_manager import *
from helpers.user_interface import *

from models.user import User
from models.exercise import Exercise


if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data"])

streamlit.title("Exercise Editor", anchor=False)
streamlit.write("""
                Select an exercise to edit its details, variations, and equipment options. <br>
                I'm trusting you with this, please don't fuck it up. <br>
                """, unsafe_allow_html=True)

user_data: User
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]

if user_data.clearanceLevel < 3:
    streamlit.error("Sorry bruv, you aren't cleared for this stuff.")
    streamlit.stop()
    
global_exercise_names: list[str] | None = None
global_exercise_list = getExerciseList()

if global_exercise_list is not None:
	global_exercise_names = [exercise.name for exercise in global_exercise_list]
else:
	global_exercise_list = []
	global_exercise_names = []


selected_exercise_name = streamlit.selectbox(
	label="Select an exercise to edit",
	options=["None"] + global_exercise_names,
    label_visibility="collapsed"
    )

if selected_exercise_name == "None":
    streamlit.stop()

selected_exercise_data = global_exercise_list[global_exercise_names.index(selected_exercise_name)]

# Display current exercise information
streamlit.subheader(f"Editing: {selected_exercise_data.name}", anchor=False)

# Create the edit form
with streamlit.form(key="exercise_editor_form", enter_to_submit=False, border=False):
    
    # Exercise category
    categories = ["Strength", "Flexibility", "Stability", "Endurance", "Functional"]
    new_category = streamlit.selectbox(
        label="Category",
        options=categories,
        index=categories.index(selected_exercise_data.category) if selected_exercise_data.category in categories else 0,
        help="The primary category this exercise falls under"
    )
    
    # Exercise variations
    streamlit.write("**Exercise Variations** (one per line)")
    variations_text = streamlit.text_area(
        label="Variations",
        value="\n".join(selected_exercise_data.variations) if selected_exercise_data.variations else "",
        help="Enter each variation on a new line",
        height=25*(len(selected_exercise_data.variations)+1),
        label_visibility="collapsed"
    )
    
    # Equipment needed
    streamlit.write("**Equipment Required** (one per line)")
    equipment_text = streamlit.text_area(
        label="Equipment (one per line)",
        value="\n".join(selected_exercise_data.equipment) if selected_exercise_data.equipment else "",
        help="Enter each piece of equipment on a new line",
        height=25*(len(selected_exercise_data.equipment)+1),
        label_visibility="collapsed"
    )
    
    submit_button = streamlit.form_submit_button(
        label="Update",
        icon=":material/save:",
        use_container_width=True
    )
    
    if submit_button:
        # Parse variations and equipment
        new_variations = [v.strip() for v in variations_text.split('\n') if v.strip()]
        new_equipment = [e.strip() for e in equipment_text.split('\n') if e.strip()]
        
        # Create updated exercise object
        updated_exercise = Exercise(
            name=selected_exercise_data.name,
            category=new_category,
            variations=new_variations,
            equipment=new_equipment,
            id=selected_exercise_data.id
        )
        
        # Attempt to update the exercise
        if updateExercise(updated_exercise):
            streamlit.success(f"Exercise '{selected_exercise_data.name}' updated successfully!")
            
            streamlit.cache_data.clear()
            streamlit.switch_page("pages/exercise/viewer.py")
        else:
            streamlit.error("Failed to update exercise. Please try again.")