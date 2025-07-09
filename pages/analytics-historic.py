from datetime import datetime
import streamlit
import pandas
from typing import List, Dict, Any
import plotly.graph_objects as go
from math import cos, pi

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

user_data: User | None

if streamlit.session_state["user_data"] is None:
    user_data = getUser(str(streamlit.user.email))
    if user_data is not None:
        streamlit.session_state["user_data"] = user_data
    else:
        streamlit.error("User data could not be loaded. Please log in again.")
        streamlit.stop()
else:
    user_data = streamlit.session_state["user_data"]

global_exercise_names: list[str] | None = None
global_exercise_list = getExerciseList()

if global_exercise_list:
    global_exercise_names = [exercise.name for exercise in global_exercise_list]
else:
    global_exercise_names = []
    streamlit.info("No exercises found in your database. Please add exercises first.")
    streamlit.stop()

selected_exercise_name = streamlit.selectbox(
    label="Select an exercise to view its history:",
    options=global_exercise_names,
    key="select_exercise_for_analytics",
    index=0
)

selected_exercise_data: Exercise | None = None
for exercise in global_exercise_list:
    if exercise.name == selected_exercise_name:
        selected_exercise_data = exercise
        break

if selected_exercise_data is None:
    streamlit.error("Selected exercise data not found. This should not happen.")
    streamlit.stop()

historical_doc = getHistoryData(user_data.id, selected_exercise_data.id) # type: ignore

if historical_doc is None or not historical_doc.exercise_sets:
    streamlit.info(f"No workout history found for '{selected_exercise_name}'.")
    streamlit.stop()

history_raw = historical_doc.exercise_sets

processed_data: List[Dict[str, Any]] = []
for entry in history_raw:
    has_valid_sets = False
    for s in entry.sets:
        if s.reps > 0 and s.weight > 0:
            has_valid_sets = True
            break

    if has_valid_sets:
        date = datetime.fromisoformat(entry.date)
        equipment = entry.equipment
        variation = entry.variation
        for s in entry.sets:
            if s.reps > 0 and s.weight > 0:
                processed_data.append({
                    'date': date,
                    'equipment': equipment,
                    'variation': variation,
                    'reps': s.reps,
                    'weight': s.weight
                })

df = pandas.DataFrame(processed_data)

if df.empty:
    streamlit.info(f"No valid sets (reps > 0 and weight > 0) found for '{selected_exercise_name}'.")
    streamlit.stop()


# --- STEP 1: Compute daily metrics ---
# Max weight per day
daily_max = df.groupby(by='date')['weight'].max().reset_index().sort_values(by='date')

# Volume moved per day
df['volume'] = df['reps'] * df['weight']
volume_per_day = df.groupby('date')['volume'].sum().reset_index().sort_values(by='date')

# --- STEP 2: Fill in missing days for max weight with cosine interpolation ---
full_date_range = pandas.date_range(start=daily_max['date'].min(), end=daily_max['date'].max())
full_df = pandas.DataFrame({'date': full_date_range})
merged = full_df.merge(daily_max, on='date', how='left')

interpolated_weights = []
dates = merged['date'].tolist()
weights = merged['weight'].tolist()

i = 0
while i < len(dates):
    if pandas.notna(weights[i]):
        interpolated_weights.append(weights[i])
        i += 1
        continue

    # Find previous known
    j = i - 1
    while j >= 0 and pandas.isna(weights[j]):
        j -= 1
    if j < 0:
        interpolated_weights.append(None)
        i += 1
        continue

    # Find next known
    k = i
    while k < len(weights) and pandas.isna(weights[k]):
        k += 1
    if k == len(weights):
        interpolated_weights.append(None)
        i += 1
        continue

    v0 = weights[j]
    v1 = weights[k]
    d0 = dates[j]
    dn = dates[k]
    total_gap = (dn - d0).days
    current_gap = (dates[i] - d0).days

    # Cosine interpolation
    weight_i = v0 + (v1 - v0) * (1 - cos(pi * current_gap / total_gap)) / 2
    interpolated_weights.append(weight_i)
    i += 1

merged['interpolated_weight'] = interpolated_weights

# --- STEP 3: Merge volume data ---
plot_df = merged.dropna(subset=['interpolated_weight']).copy()
plot_df = plot_df.merge(volume_per_day, on='date', how='left')

plot_df['is_actual'] = plot_df['weight'].notna()
plot_df['actual_weight'] = plot_df['weight'].fillna(method='ffill')

# --- STEP 4: Plot everything ---
fig = go.Figure()

# Smoothed line (spline)
fig.add_trace(go.Scatter(
    x=plot_df['date'],
    y=plot_df['interpolated_weight'],
    mode='lines',
    name='Smoothed Max Weight',
    line=dict(color='rgba(255, 145, 164, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Interpolated: %{y:.1f} kg',
))

# Volume moved (secondary Y-axis)
fig.add_trace(go.Scatter(
    x=plot_df[plot_df['volume'].notna()]['date'],
    y=plot_df[plot_df['volume'].notna()]['volume'],
    mode='lines',
    name='Volume Moved',
    yaxis='y2',
    line=dict(color='rgba(0, 128, 128, 1)', width=3, shape='spline'),
    hovertemplate='%{x|%b %d, %Y}<br>Volume: %{y:.0f} kg',
))

# --- STEP 5: Final Layout ---
fig.upandasate_layout(
    title=f"Smoothed Progress for {selected_exercise_name}",
    xaxis_title='Date',
    yaxis_title='Max Weight (kg)',
    yaxis2=dict(
        title='Volume Moved (kg)',
        overlaying='y',
        side='right',
        showgrid=False,
        visible=True,
    ),
    template='simple_white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=60, b=40),
    height=550
)

streamlit.plotly_chart(fig, use_container_width=True)