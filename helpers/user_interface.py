import streamlit

APP_TITLE = "Fitness Tracker"
APP_ICON = ":material/fitness_center:"

def uiSetup():
	columnWidthHack()


# There is a known issue with streamlit columns on mobile devices.
def columnWidthHack():
	streamlit.markdown("""
		<style>
			[data-testid="stColumn"] {
    			width: calc(33.3333% - 1rem) !important;
    			flex: 1 1 calc(33.3333% - 1rem) !important;
    			min-width: calc(33% - 1rem) !important;
			}
			[data-testid="stHorizontalBlock"] {
                gap: 0.2rem !important;
            }
			/* iOS Safari zooms into inputs with a font size below 16px */
			input, textarea, select {
				font-size: 16px !important;
			}
		</style>
						""", unsafe_allow_html=True)
	

def setupNavigation():
	home_page = streamlit.Page(page="home.py", title="Home", icon=":material/fitness_center:")

# Exercises
	editor = streamlit.Page(page="pages/exercise/editor.py", title="Manage", icon=":material/construction:")
	adder = streamlit.Page(page="pages/exercise/adder.py", title="Create", icon=":material/library_add:")

# Routines
	manager = streamlit.Page(page="pages/routine/manager.py", title="Manage", icon=":material/construction:")
	creator = streamlit.Page(page="pages/routine/creator.py", title="Create", icon=":material/library_add:")

# Strength Training
	workout = streamlit.Page(page="pages/strength-training/workout.py", title="Record a Session", icon=":material/exercise:")
	post_workout = streamlit.Page(page="pages/strength-training/post-workout.py", title="Workout Analytics", icon=":material/candlestick_chart:")
	historical = streamlit.Page(page="pages/strength-training/historic.py", title="Historical Analytics", icon=":material/trending_up:")

# User Profile Management
	profile = streamlit.Page(page="pages/user/profile.py", title="Management", icon=":material/account_box:")

	nav_bar = streamlit.navigation(
		pages={
			"": [home_page],
			"Exercises": [editor, adder],
			"Routines": [manager, creator],
			"Strength Training": [workout, post_workout, historical],
			"User Account": [profile]
		},
		position="sidebar",
		expanded=True
	)

	nav_bar.run()
