import streamlit

def uiSetup():
	columnWidthHack()
	hideSidebar()
	actualSidebar()

def actualSidebar():
	with streamlit.sidebar:
		streamlit.page_link("Fitness Tracker.py", label="Home Page", icon=":material/home:")
		streamlit.divider()
		streamlit.page_link("pages/routine-manager.py", label="Manage Your Routines", icon=":material/construction:")
		streamlit.page_link("pages/routine-creator.py", label="Create a New Routine", icon=":material/add_notes:")
		streamlit.divider()
		streamlit.page_link("pages/workout-recorder.py", label="Record a Workout", icon=":material/exercise:")
		streamlit.divider()
		streamlit.page_link("pages/analytics-historic.py", label="Historical Workout Analytics", icon=":material/table_chart_view:")
		streamlit.divider()


		if not streamlit.user.is_logged_in:
			streamlit.warning("You'll need to log in to continue")
			if streamlit.button("Login with Google", icon=":material/login:"):
				streamlit.login()
		else:
			streamlit.page_link("pages/profile-manager.py", label="User Profile Management", icon=":material/account_box:")
			if streamlit.button("Logout", icon=":material/logout:"):
				streamlit.logout()


# There is a known issue with streamlit columns on mobile devices.
# This is just a quick CSS hack for it.
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
		</style>
						""", unsafe_allow_html=True)

def hideSidebar():
	streamlit.markdown("""
		<style>
			[data-testid="stSidebarNav"] {	display: none !important;	}
			[data-testid="stSidebarContent"] {	padding-top: 0px;	}
		</style>
						""", unsafe_allow_html=True)