import streamlit

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import getBasicUser, getRoutinesList, getWorkoutSessionData
from database.read import getExerciseList, getExerciseNames, getExerciseData

from database.create import createWorkout, createWorkoutSession
from database.delete import deleteSession
from database.update import updateWorkoutSession, updateExerciseHistory

from models.user import BasicUser
from models.routines import Routine
from models.session import WorkoutSession, WorkoutExercise, WorkoutSet

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", "workout_session_data", "current_exercise_index", "add_exercise_dialog"])

streamlit.title("Workout Recorder", anchor=False)

workout_session_data: WorkoutSession | None

user_data: BasicUser
if streamlit.session_state["user_data"] is None:
    streamlit.session_state["user_data"] = getBasicUser(str(streamlit.user.email))
user_data = streamlit.session_state["user_data"]
    
if user_data.clearanceLevel < 1:
    accessControlWarning()
    getInTouch()
    streamlit.stop()

if streamlit.session_state["workout_session_data"] is None:
    workout_session_data = getWorkoutSessionData(user_data.id)
    if workout_session_data is not None:
        streamlit.session_state["workout_session_data"] = workout_session_data
        streamlit.session_state["current_exercise_index"] = workout_session_data.exercise_index
    else:
        streamlit.session_state["workout_session_data"] = None
        streamlit.session_state["current_exercise_index"] = -1
else:
    workout_session_data = streamlit.session_state["workout_session_data"]

if streamlit.session_state["add_exercise_dialog"] is None:
    streamlit.session_state["add_exercise_dialog"] = False

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
            selected_exercise_data = global_exercise_list[global_exercise_names.index(selected_exercise_name)]
            new_exercise = WorkoutExercise(
                exercise_id=selected_exercise_data.id,
                variation="None",
                equipment="None",
                sets=[WorkoutSet(reps=8, weight=0.0), WorkoutSet(reps=8, weight=0.0), WorkoutSet(reps=8, weight=0.0)]
            )
            streamlit.session_state["workout_session_data"].exercises.append(new_exercise)

            streamlit.session_state["current_exercise_index"] = len(streamlit.session_state["workout_session_data"].exercises) - 1

            if updateWorkoutSession(streamlit.session_state["workout_session_data"]):
                streamlit.rerun()

def switchExerciseCallback():
    selected_exercise_identifier = streamlit.session_state["active_exercise_select"]

    if selected_exercise_identifier == "Add New Exercise...":
        streamlit.session_state["add_exercise_dialog"] = True
        return

    current_workout: WorkoutSession = streamlit.session_state["workout_session_data"]

    # Create unique identifiers for each exercise (name + variation + equipment)
    current_exercise_identifiers = [
        f"{getExerciseNames([exercise.exercise_id])[0]} ({exercise.variation}, {exercise.equipment})"
        for exercise in current_workout.exercises
    ]

    # Find the index of the selected exercise based on its unique identifier
    try:
        selected_exercise_index = current_exercise_identifiers.index(selected_exercise_identifier)
    except ValueError:
        streamlit.error("Selected exercise not found.")
        return

    # Update session state and workout session data
    streamlit.session_state["current_exercise_index"] = selected_exercise_index
    current_workout.exercise_index = selected_exercise_index
    updateWorkoutSession(current_workout)

is_workout_active = workout_session_data is not None

if is_workout_active:
    workout_exercise_identifiers = [
        f"{getExerciseNames([exercise.exercise_id])[0]} ({exercise.variation}, {exercise.equipment})"
        for exercise in workout_session_data.exercises
    ]

    current_exercise_index: int = streamlit.session_state["current_exercise_index"]

    selected_exercise_identifier = streamlit.selectbox(
        label="Select An Exercise",
        options=workout_exercise_identifiers + ["Add New Exercise..."],
        index=current_exercise_index,
        on_change=switchExerciseCallback,
        key="active_exercise_select"
    )

    if streamlit.session_state["add_exercise_dialog"]:
        addExerciseDialog()
        streamlit.session_state["add_exercise_dialog"] = False

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
                        label_visibility="collapsed"
                    )

            streamlit.markdown("---")

            col_add_set, col_drop_set, col_update_info = streamlit.columns([1, 1, 1])

            if col_add_set.form_submit_button("Add", use_container_width=True, icon=":material/add:"):
                current_exercise.sets.append(
                    WorkoutSet(reps=current_exercise.sets[0].reps if current_exercise.sets else 8, weight=0.0)
                )
                if updateWorkoutSession(streamlit.session_state["workout_session_data"]):
                    streamlit.rerun()
                else:
                    streamlit.error("Failed to update session information.")

            if col_drop_set.form_submit_button("Drop", use_container_width=True, icon=":material/delete:"):
                if current_exercise.sets:
                    current_exercise.sets.pop() 
                    if updateWorkoutSession(streamlit.session_state["workout_session_data"]):
                        streamlit.rerun()
                    else:
                        streamlit.error("Failed to update session information.")
                else:
                    streamlit.warning("No sets to drop.")

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
            result = updateWorkoutSession(streamlit.session_state["workout_session_data"])
            if not result:
                streamlit.error("Something broke...")
                streamlit.stop()

            workoutID = createWorkout(streamlit.session_state["workout_session_data"].id)
            if workoutID is None:
                streamlit.error("Couldn't save workout.")
                streamlit.stop()

            result = deleteSession(streamlit.session_state["workout_session_data"].id)
            if not result:
                streamlit.error("Couldn't clear session data.")
                streamlit.stop()
            
            updateExerciseHistory(user_data.id, workoutID)

            streamlit.success("Workout saved to disk. Re-directing!")
            clearSessionVariable(["workout_session_data", "current_exercise_index", "add_exercise_dialog", "workout_exercise_selection"])
            streamlit.switch_page("pages/analytics/post-workout.py")


    with col_cancel_workout.expander("Cancel Workout", expanded=False, icon=":material/cancel:"):
        streamlit.warning("This will erase your current progress.")
        if streamlit.button("Confirm", key="cancel-workout-btn"):
            result = updateWorkoutSession(streamlit.session_state["workout_session_data"])
            if not result:
                streamlit.error("Something broke...")
                streamlit.stop()

            result = deleteSession(streamlit.session_state["workout_session_data"].id)
            if not result:
                streamlit.error("Couldn't clear session data.")
                streamlit.stop()

            streamlit.success("Workout cancelled. All progress discarded!")
            clearSessionVariable(["workout_session_data", "current_exercise_index", "add_exercise_dialog", "workout_exercise_selection"])
            streamlit.rerun()             

else:
    streamlit.write("Select a workout routine to get started.")

    user_routines = getRoutinesList(user_data.id)
    if user_routines is None or user_routines == []:
        streamlit.info("You don't seem to have any routines set up. Please create one to access it here.")
        streamlit.stop()

    user_routine_names: List[str] = ["None"] + [routine.name for routine in user_routines]

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
            selected_routine: Routine = user_routines[user_routine_names.index(selected_routine_name) - 1]

            if selected_routine and selected_routine.id:

                new_workout_session = createWorkoutSession(user_data.id, selected_routine.id)
                if new_workout_session:
                    streamlit.session_state["workout_session_data"] = getWorkoutSessionData(user_data.id)
                    streamlit.session_state["current_exercise_index"] = 0
                    streamlit.success(f"Workout '{selected_routine.name}' started!")
                    streamlit.rerun()
                else:
                    streamlit.error("Failed to start workout session. Please try again.")
        else:
            streamlit.warning("Please select a routine to start.")