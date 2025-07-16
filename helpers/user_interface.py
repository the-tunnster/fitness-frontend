import streamlit

def uiSetup():
	columnWidthHack()
	loginLogoutStuff()


def loginLogoutStuff():
	with streamlit.sidebar:

		if not streamlit.user.is_logged_in:
			streamlit.warning("You'll need to log in to continue")
			if streamlit.button("Login with Google", icon=":material/login:"):
				streamlit.login()
		else:
			if streamlit.button("Logout", icon=":material/logout:"):
				streamlit.logout()


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
		</style>
						""", unsafe_allow_html=True)
	

def setupNavigation():
	home_page = streamlit.Page(page="home.py", title="Home", icon=":material/home:")

	manager = streamlit.Page(page="pages/routine/manager.py", title="Management", icon=":material/construction:")
	creator = streamlit.Page(page="pages/routine/creator.py", title="Creation", icon=":material/add_notes:")

	workout = streamlit.Page(page="pages/recorder/workout.py", title="Strength Training", icon=":material/exercise:")
	cardio = streamlit.Page(page="pages/recorder/cardio.py", title="Cardiovascular", icon=":material/sprint:")

	post_workout = streamlit.Page(page="pages/analytics/post-workout.py", title="Post Workout", icon=":material/table_chart_view:")
	post_cardio = streamlit.Page(page="pages/analytics/post-cardio.py", title="Cardiovascular", icon=":material/table_chart_view:")
	historical = streamlit.Page(page="pages/analytics/historic.py", title="Historical", icon=":material/table_chart_view:")

	profile = streamlit.Page(page="pages/user/profile.py", title="Management", icon=":material/account_box:")

	nav_bar = streamlit.navigation(
		pages={
			"": [home_page],
			"Routines": [manager, creator],
			"Record A Session": [workout, cardio],
			"Analytics": [post_workout, post_cardio, historical],
			"Account": [profile]
		},
		position="sidebar",
		expanded=True
	)

	nav_bar.run()