import streamlit
import plotly.graph_objects as go                                                                                   # type:ignore

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *

streamlit.set_page_config(
    page_title="Analytics",
    page_icon=":material/table_chart_view:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", ])

streamlit.header("Historical Workout Analytics", anchor=False)

# --- Load user data ---
user_data: User | None = streamlit.session_state["user_data"]
if user_data is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded. Please log in again.")
        streamlit.stop()

workout_count = checkWorkoutCount(user_data.id)
if workout_count < 15 :
    streamlit.progress(
        text="You need at least 15 workouts recorded.",
        value=(1/15)*workout_count
        )
    streamlit.info("You don't have enough workouts to display any useful data. Here's mine instead.")


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
if workout_count < 15 :
    historic_data = getHistoryData('68674a2e19fc0c426e3ece85', selected_exercise_data.id)
else:
    historic_data = getHistoryData(user_data.id, selected_exercise_data.id)

if not historic_data:
    streamlit.info(f"No workout history found for '{selected_exercise_name}'.")
    streamlit.stop()

if len(historic_data) <= 1:
    streamlit.info(f"Not enough valid data found for '{selected_exercise_name}'.")
    streamlit.stop()


# --- Plotting ---
fig = go.Figure()

# Max Weight (Primary Axis)
fig.add_trace(go.Scatter(                                                                                           # type:ignore
    x=[entry['date'] for entry in historic_data],
    y=[entry['interpolated_weight'] for entry in historic_data],
    mode='lines',
    name='Max Weight             ',
    line=dict(color='rgba(255, 145, 164, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Interpolated: %{y:.1f} kg',
)) 

# Volume Moved (Secondary Axis)
fig.add_trace(go.Scatter(                                                                                           # type:ignore
    x=[entry['date'] for entry in historic_data if 'volume' in entry],
    y=[entry['volume'] for entry in historic_data if 'volume' in entry],
    mode='lines',
    name='Volume Moved',
    yaxis='y2',
    line=dict(color='rgba(0, 128, 128, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Volume: %{y:.0f} kg',
))

fig.update_layout(                                                                                                  # type:ignore
    xaxis=dict(
        fixedrange=True
    ),
    yaxis=dict(
        fixedrange=True,
        dtick=None,  # Auto-spacing to prevent overlap
        gridcolor='rgba(0,0,0,0.1)',
        ticks='inside',
        tickfont=dict(size=10),
        tickmode='auto',  # Auto-choose tick spacing
        nticks=5  # Limit number of ticks
    ),
    yaxis2=dict(
        overlaying='y',
        side='left',
        showgrid=False,
        fixedrange=True,
        dtick=None,  # Auto-spacing to prevent overlap
        ticks='inside',
        tickcolor='rgba(0, 0, 0, 1)',
        tickfont=dict(size=10),
        anchor='free',
        position=1,  # Offset slightly from primary axis
        tickmode='auto',  # Auto-choose optimal tick spacing
        nticks=5  # Limit number of ticks
    ),
    template='simple_white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5,
        itemsizing="constant",  # Keep legend items consistent
        itemwidth=30,  # Increase spacing between legend items
        font=dict(size=12),
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

streamlit.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})                             # type:ignore