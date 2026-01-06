import streamlit

from helpers.state_manager import AppState
from helpers.user_interface import *

from database.read import getBasicUser, getRoutinesList, getWorkoutSessionData
from database.read import getExerciseList, getExerciseData

from database.create import createWorkout, createWorkoutSession
from database.delete import deleteSession
from database.update import updateWorkoutSession, updateExerciseHistory

from models.user import BasicUser
from models.session import WorkoutSession, WorkoutExercise, WorkoutSet

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
state = AppState()

streamlit.title("Workout Recorder", anchor=False)

workout_session_data: WorkoutSession | None

user_data: BasicUser
if state.user is None:
    state.user = getBasicUser(str(streamlit.user.email))
    if state.user is None or state.user.clearance_level < 1:
        accessControlWarning()
        getInTouch()
        streamlit.stop()
user_data = state.user

if state.workout_session is None:
    workout_session_data = getWorkoutSessionData(user_data.id)
    if workout_session_data is not None:
        state.workout_session = workout_session_data
        state.current_exercise_index = workout_session_data.exercise_index
    else:
        state.workout_session = None
        state.current_exercise_index = -1
else:
    workout_session_data = state.workout_session

if state.is_add_dialog_open:
    state.is_add_dialog_open = False

@streamlit.dialog("Add an Exercise to your Workout")
def addExerciseDialog():
    global_exercise_names: list[str] | None = None
    global_exercise_list = getExerciseList()

    if global_exercise_list is not None:
        global_exercise_names = [exercise.name for exercise in global_exercise_list]
    else:
        global_exercise_list = []
        global_exercise_names = []

    with streamlit.form("add_exercise_dialog_form", clear_on_submit=True, enter_to_submit=False):
        selected_exercise_name = streamlit.selectbox(
            label="Select a new exercise to add",
            options=global_exercise_names,
            key="dialog_select_exercise"
        )
    
        if streamlit.form_submit_button("Add exercise", use_container_width=True):
            if state.workout_session is None:
                streamlit.error("No active workout session.")
                return 

            selected_exercise_data = global_exercise_list[global_exercise_names.index(selected_exercise_name)]
            new_exercise = WorkoutExercise(
                exercise_id=selected_exercise_data.id,
                variation="None",
                equipment="None",
                sets=[WorkoutSet(reps=8, weight=0.0), WorkoutSet(reps=8, weight=0.0), WorkoutSet(reps=8, weight=0.0)],
                name=selected_exercise_data.name
            )
            state.workout_session.add_exercise(new_exercise)
            state.current_exercise_index = state.workout_session.exercise_index

            if updateWorkoutSession(state.workout_session):
                streamlit.rerun()

def switchExerciseCallback():
    selection = state.workout_exercise_selection

    if selection == "Add New Exercise...":
        state.is_add_dialog_open = True
        return
    
    if state.workout_session is None:
        return

    # Update session state and workout session data
    try:
        selected_exercise_index = state.workout_session.exercises.index(selection)
        state.current_exercise_index = selected_exercise_index
        state.workout_session.exercise_index = selected_exercise_index
        updateWorkoutSession(state.workout_session)
    except ValueError:
        streamlit.error("Selected exercise not found.")

is_workout_active = workout_session_data is not None

if is_workout_active and workout_session_data:
    options = workout_session_data.exercises + ["Add New Exercise..."]

    current_exercise_index: int = state.current_exercise_index

    # If the index is out of bounds (e.g. -1), default to 0
    box_index = current_exercise_index if current_exercise_index >= 0 and current_exercise_index < len(workout_session_data.exercises) else 0
    print(box_index)

    selected_exercise = streamlit.selectbox(
        label="Select An Exercise",
        options=options,
        index=box_index,
        format_func=lambda x: x.display_name if isinstance(x, WorkoutExercise) else x,
        on_change=switchExerciseCallback,
        key="workout_exercise_selection"
    )

    if state.is_add_dialog_open:
        addExerciseDialog()
        state.is_add_dialog_open = False

    current_exercise = workout_session_data.exercises[current_exercise_index]
    
    if current_exercise:
        with streamlit.form("exercise_recording_form", clear_on_submit=False, enter_to_submit=False, border=False):
            exercise_metadata = getExerciseData(current_exercise.exercise_id)

            if exercise_metadata:
                variation_options = exercise_metadata.variations
                equipment_options = exercise_metadata.equipment
            else:
                variation_options = ["None"]
                equipment_options = ["None"]

            col_variation, col_equipment = streamlit.columns([1, 1])
            with col_variation:
                current_exercise.variation = streamlit.selectbox(
                    label="Variation",
                    options=variation_options,
                    index=variation_options.index(current_exercise.variation) if current_exercise.variation in variation_options else 0,
                    key=f"variation_select_{current_exercise.exercise_id}"
                )
            with col_equipment:
                current_exercise.equipment = streamlit.selectbox(
                    label="Equipment",
                    options=equipment_options,
                    index=equipment_options.index(current_exercise.equipment) if current_exercise.equipment in equipment_options else 0,
                    key=f"equipment_select_{current_exercise.exercise_id}"
                )

            streamlit.subheader("Sets", anchor=False)

            col_header_reps, col_header_weight = streamlit.columns([1, 1])
            with col_header_reps: streamlit.write("Reps")
            with col_header_weight: streamlit.write("Weight")

            for set_index, workout_set in enumerate(current_exercise.sets):
                col_reps, col_weight = streamlit.columns([1, 1])

                with col_reps:
                    workout_set.reps = streamlit.number_input(
                        f"Reps Set {set_index + 1}",
                        value=int(workout_set.reps),
                        min_value=0,
                        key=f"reps_{current_exercise.exercise_id}_{set_index}",
                        label_visibility="collapsed"
                    )
                with col_weight:
                    workout_set.weight = streamlit.number_input(
                        f"Weight Set {set_index + 1}",
                        value=float(workout_set.weight),
                        min_value=0.0,
                        step=0.5,
                        key=f"weight_{current_exercise.exercise_id}_{set_index}",
                        label_visibility="collapsed",
                        help="Barbell + Plates = Total, Dumbbells/Kettlebells = Individual"
                    )

            streamlit.markdown("---")

            col_add_set, col_drop_set, col_update_info = streamlit.columns([1, 1, 1])

            if col_add_set.form_submit_button("Add", use_container_width=True, icon=":material/add:"):
                current_exercise.add_set(
                    reps=current_exercise.sets[0].reps if current_exercise.sets else 8, weight=0.0
                )
                if updateWorkoutSession(workout_session_data):
                    streamlit.rerun()
                else:
                    streamlit.error("Failed to update session information.")

            if col_drop_set.form_submit_button("Drop", use_container_width=True, icon=":material/remove:"):
                current_exercise.drop_set()
                if updateWorkoutSession(workout_session_data):
                    streamlit.rerun()
                else:
                    streamlit.error("Failed to update session information.")

            if col_update_info.form_submit_button("Update", use_container_width=True, icon=":material/upgrade:"):
                if updateWorkoutSession(workout_session_data):
                    streamlit.rerun()
                else:
                    streamlit.error("Failed to update exercise information.")
    
    streamlit.divider()

    col_end_workout, col_cancel_workout = streamlit.columns(2)

    with col_end_workout.expander("Finish Workout", expanded=False, icon=":material/save:"):
        streamlit.warning("This will commit your routine to disk.")
        if streamlit.button("Confirm", key="finish-workout-btn"):
            result = updateWorkoutSession(workout_session_data)
            if not result:
                streamlit.error("Something broke...")
                streamlit.stop()

            if not workout_session_data.id:
                streamlit.error("Session ID is invalid.")
                streamlit.stop()

            workoutID = createWorkout(workout_session_data.id, user_data.id)
            if workoutID is None:
                streamlit.error("Couldn't save workout.")
                streamlit.stop()

            result = deleteSession(workout_session_data.id)
            if not result:
                streamlit.error("Couldn't clear session data.")
                streamlit.stop()
            
            updateExerciseHistory(user_data.id, workoutID)

            streamlit.success("Workout saved to disk. Re-directing!")
            state.reset_workout_state()
            streamlit.switch_page("pages/strength-training/post-workout.py")


    with col_cancel_workout.expander("Cancel Workout", expanded=False, icon=":material/cancel:"):
        streamlit.warning("This will erase your current progress.")
        if streamlit.button("Confirm", key="cancel-workout-btn"):
            result = updateWorkoutSession(workout_session_data)
            if not result:
                streamlit.error("Something broke...")
                streamlit.stop()

            if not workout_session_data.id:
                 streamlit.error("Invalid session ID")
                 streamlit.stop()

            result = deleteSession(workout_session_data.id)
            if not result:
                streamlit.error("Couldn't clear session data.")
                streamlit.stop()

            streamlit.success("Workout cancelled. All progress discarded!")
            state.reset_workout_state()
            streamlit.rerun()             

else:
    streamlit.write("Select a workout routine to get started.")

    user_routines = getRoutinesList(user_data.id)
    if user_routines is None or user_routines == []:
        streamlit.info("You don't seem to have any routines set up. Please create one to access it here.")
        streamlit.stop()

    user_routine_names: list[str] = ["None"] + [routine.name for routine in user_routines]

    selected_routine_name: str = streamlit.selectbox(
        label="Select a routine",
        options=user_routine_names,
        index=0,
        key="start_routine_select",
        label_visibility="collapsed"
    )

    start_workout_button_disabled = (selected_routine_name == "None")

    if streamlit.button("Start Workout", disabled=start_workout_button_disabled, use_container_width=True, type="primary", icon=":material/play_arrow:"):
        if selected_routine_name != "None":
            routine_id = user_routines[user_routine_names.index(selected_routine_name) - 1].id

            new_workout_session = createWorkoutSession(user_data.id, routine_id)
            if new_workout_session:
                state.workout_session = getWorkoutSessionData(user_data.id)
                state.current_exercise_index = 0
                streamlit.rerun()
            else:
                streamlit.error("Failed to start workout session. Please try again.")
        else:
            streamlit.warning("Please select a routine to start.")