HOST = "http://localhost"
PORT = ":8080"

BASE_URL = HOST+PORT

USER_URLS = {
	"me": BASE_URL + "/me",
	"create": BASE_URL + "/user/create",
	"update": BASE_URL + "/user/update",
}

EXERCISE_URLS = {
	"id": BASE_URL + "/exercise/id",
	"name": BASE_URL + "/exercise/name",
	"list": BASE_URL + "/exercise/list",
	"data": BASE_URL + "/exercise/data",
	"create": BASE_URL + "/exercise/create",
	"update": BASE_URL + "/exercise/update",
}

ROUTINE_URLS = {
	"list": BASE_URL + "/routines/list",
	"data": BASE_URL + "/routines/data",
	"create": BASE_URL + "/routines/create",
	"update": BASE_URL + "/routines/update",
	"delete": BASE_URL + "/routines/delete",
}

WORKOUT_URLS = {
	"list": BASE_URL + "/workouts/list",
	"data": BASE_URL + "/workouts/data",
	"count": BASE_URL + "/workouts/count",
	"create": BASE_URL + "/workouts/create",
}

SESSION_URLS = {
	"data": BASE_URL + "/session/data",
	"create": BASE_URL + "/session/create",
	"update": BASE_URL + "/session/update",
	"delete": BASE_URL + "/session/delete",
}

HISTORY_URLS = {
	"data": BASE_URL + "/history/data",
	"create": BASE_URL + "/history/create",
	"update": BASE_URL + "/history/update",
}