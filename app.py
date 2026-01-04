# type: ignore

import streamlit
import plotly.graph_objects as go

from helpers.user_interface import *

from database.read import getExerciseList

streamlit.set_page_config(layout="wide")

getExerciseList()

setupNavigation()