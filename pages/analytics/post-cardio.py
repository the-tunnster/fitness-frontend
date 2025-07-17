import streamlit
import plotly.graph_objects as go                                                                                   # type:ignore

from helpers.cache_manager import *
from helpers.user_interface import *

from database.read import *

streamlit.set_page_config(
    page_title="Post Cardio Analysis",
    page_icon=":material/table_chart_view:",
    layout="wide",
)

if not streamlit.user.is_logged_in:
    streamlit.switch_page("home.py")

uiSetup()
initSessionState(["user_data", ])

streamlit.header("Cardio History", anchor=False)

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
    label="Select an exercise to view its history:",
    options=cardio_names,
    key="select_exercise_for_analytics",
    index=0
)

if selected_cardio_name == "None":
    streamlit.stop()

selected_cardio_data = cardio_list[cardio_names.index(selected_cardio_name) - 1]

data: list[dict[str, Any]] | None = getCardioHistoryData(user_data.id, selected_cardio_data.id)
if data is None:
    streamlit.info("You don't have enough workouts to display any useful data. Hit the gym bruv.")
    streamlit.stop()

fig = go.Figure()

# Extracting data for plotting
dates = [session['date'] for session in data['sessions']]                                                            # type:ignore
total_distances = [session['metrics']['total_distance'] for session in data['sessions']]                             # type:ignore
total_times = [session['metrics']['total_time'] for session in data['sessions']]                                     # type:ignore

# Total Distance (Primary Axis)                                                     
fig.add_trace(go.Scatter(                                                                                            # type:ignore
    x=dates,
    y=total_distances,
    mode='lines',
    name='Total Distance',
    line=dict(color='rgba(255, 145, 164, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Distance: %{y:.0f} m', # Assuming meters
))

# Total Time (Secondary Axis)
fig.add_trace(go.Scatter(                                                                                            # type:ignore
    x=dates,
    y=total_times,
    mode='lines',
    name='Total Time',
    yaxis='y2', # Assign to the secondary y-axis
    line=dict(color='rgba(0, 128, 128, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Time: %{y:.0f} sec', # Assuming seconds
))

fig.update_layout(                                                                                                   # type:ignore
    xaxis=dict(
        fixedrange=True
    ),
    yaxis=dict(
        fixedrange=True,
        dtick=None,
        gridcolor='rgba(0,0,0,0.1)',
        ticks='inside',
        tickfont=dict(size=10),
        tickmode='auto',
        nticks=5,
        title_text='Total Distance (m)' # Label for the primary y-axis
    ),
    yaxis2=dict(
        overlaying='y',
        side='left',
        showgrid=False,
        fixedrange=True,
        dtick=None,
        ticks='inside',
        tickcolor='rgba(0, 0, 0, 1)',
        tickfont=dict(size=10),
        anchor='free',
        position=1,
        tickmode='auto',
        nticks=5,
        title_text='Total Time (sec)' # Label for the secondary y-axis
    ),
    template='simple_white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5,
        itemsizing="constant",
        itemwidth=30,
        font=dict(size=12),
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

# Display the chart in Streamlit
streamlit.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})                              # type:ignore