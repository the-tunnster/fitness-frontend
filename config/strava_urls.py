import streamlit

AUTH_URL = (f"https://www.strava.com/oauth/authorize"
			f"?client_id={streamlit.secrets["strava"]["client_id"]}"
			f"&redirect_uri=http://localhost:8501/cardio"
			f"&response_type=code"
			f"&approval_prompt=auto"
			f"&scope=activity:read_all,profile:read_all"
			)

TOKEN_GRANT_URL = (f"https://www.strava.com/api/v3/oauth/token"
				   f"?client_id={streamlit.secrets["strava"]["client_id"]}"
				   f"&client_secret={streamlit.secrets["strava"]["client_secret"]}"
				   f"&grant_type=authorization_code"
				   )

TOKEN_REFRESH_URL= (f"https://www.strava.com/oauth/token"
					f"?client_id={streamlit.secrets["strava"]["client_id"]}"
				    f"&client_secret={streamlit.secrets["strava"]["client_secret"]}"
					f"?grant_type=refresh_token"
					)