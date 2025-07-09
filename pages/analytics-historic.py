import streamlit
import pandas
import plotly.graph_objects as go

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *

streamlit.set_page_config(
    page_title="Analytics",
    page_icon=":material/table_chart_view:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("./Fitness Tracker.py")

uiSetup()
initSessionState()

streamlit.header("Historical Workout Analytics", anchor=False)

# --- Load user data ---
user_data: User | None = streamlit.session_state.get("user_data")
if user_data is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded. Please log in again.")
        streamlit.stop()

# --- Load exercises ---
global_exercise_list = getExerciseList()
if not global_exercise_list:
    streamlit.info("No exercises found in your database. Please add exercises first.")
    streamlit.stop()

global_exercise_names = [exercise.name for exercise in global_exercise_list]

selected_exercise_name = streamlit.selectbox(
    label="Select an exercise to view its history:",
    options=global_exercise_names,
    key="select_exercise_for_analytics",
    index=0
)

selected_exercise_data = next(
    (exercise for exercise in global_exercise_list if exercise.name == selected_exercise_name),
    None
)

if selected_exercise_data is None:
    streamlit.error("Selected exercise data not found. This should not happen.")
    streamlit.stop()

# --- Fetch processed history data ---
historic_data = getHistoryData(user_data.id, selected_exercise_data.id)  # type: ignore

if historic_data is None:
    streamlit.info(f"No workout history found for '{selected_exercise_name}'.")
    streamlit.stop()

if historic_data.empty:
    streamlit.info(f"No valid sets (reps > 0 and weight > 0) found for '{selected_exercise_name}'.")
    streamlit.stop()

# --- Plotting ---
fig = go.Figure()

# Smoothed Max Weight
fig.add_trace(go.Scatter( 
    x=historic_data['date'],
    y=historic_data['interpolated_weight'],
    mode='lines',
    name='Max Weight',
    line=dict(color='rgba(255, 145, 164, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Interpolated: %{y:.1f} kg',
)) 

# Volume Moved (Secondary Axis)
fig.add_trace(go.Scatter(
    x=historic_data[historic_data['volume'].notna()]['date'],
    y=historic_data[historic_data['volume'].notna()]['volume'],
    mode='lines',
    name='Volume Moved',
    yaxis='y2',
    line=dict(color='rgba(0, 128, 128, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Volume: %{y:.0f} kg',
))

fig.update_layout(
    yaxis2=dict(
        overlaying='y',
        side='left',
        showgrid=False,
        visible=True,
    ),
    template='simple_white',
    legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

streamlit.plotly_chart(fig, use_container_width=True)