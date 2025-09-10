import streamlit

def uiSetup():
	columnWidthHack()
	loginLogoutStuff()


def loginLogoutStuff():
	with streamlit.sidebar:

		if not streamlit.user.is_logged_in:
			streamlit.warning("You'll need to log in to continue")
			if streamlit.button("Login with Google", icon=":material/login:", use_container_width=True):
				streamlit.login()
		else:
			if streamlit.button("Logout", icon=":material/logout:", use_container_width=True):
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

# Cardio vis Strava
	cardio = streamlit.Page(page="pages/cardio/import-data.py", title="Import Data", icon=":material/sprint:")
	post_cardio = streamlit.Page(page="pages/cardio/post-cardio.py", title="Activity Analytics", icon=":material/trending_up:")

# User Profile Management
	profile = streamlit.Page(page="pages/user/profile.py", title="Management", icon=":material/account_box:")

	nav_bar = streamlit.navigation(
		pages={
			"": [home_page],
			"Exercises": [editor, adder],
			"Routines": [manager, creator],
			"Strength Training": [workout, post_workout, historical],
			"Strava": [cardio, post_cardio],
			"User Account": [profile]
		},
		position="sidebar",
		expanded=True
	)

	nav_bar.run()

def accessControlWarning():
	streamlit.write("""
	I've started to implement an access control system. <br>
	If you're seeing this page, it might be a bug I need to fix.<br> 
	Reach out and let me know. <br>
	""", unsafe_allow_html=True)

def getInTouch():
	col1, col2 = streamlit.columns([1, 1])
	col1.link_button(label="Instagram DM", url="https://www.instagram.com/the_tunnster/", icon=":material/chat:")
	col2.link_button(label="Call", url="tel:+61493648088", icon=":material/add_call:")