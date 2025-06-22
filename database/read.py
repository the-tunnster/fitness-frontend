import requests
import streamlit

from models.user import *
from models.routines import *
from models.exercise import *
from models.workouts import *

def getUser(emailID: str) -> User | None :
    try:
        response = requests.request(
            method="GET",
            url="http://localhost:8080/me",
            params={"email": emailID}
        )

        if response.json()["id"] == "000000000000000000000000":
            return None
    except:
        return None

    user = User(**response.json())
	
    return user

@streamlit.cache_data
def getExerciseList() -> list[Routine] | None :
    try:
        response = requests.get(f"http://localhost:8080/exercise/list")
        
        if response.status_code == 200:
            exercises = [Exercise(**item) for item in response.json()]
            return exercises
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None
    
def getExerciseNames(exercise_ids: list[str]) -> list[str] | None:
    try:
        params = [("exercise_id", eid) for eid in exercise_ids]
        response = requests.get("http://localhost:8080/exercise/name", params=params)

        print(f"Final URL: {response.url}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} — {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None

def getExerciseIDs(exercise_names: list[str]) -> list[str] | None:
    try:
        params = [("exercise_name", name) for name in exercise_names]
        response = requests.get("http://localhost:8080/exercise/id", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} — {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None

def getRoutinesList(user_id: str) -> list[Routine] | None :
    try:
        response = requests.get(f"http://localhost:8080/routines/list", params={"user_id": user_id})
        
        if response.json() is None:
            return None

        if response.status_code == 200:
            routines = [Routine(**item) for item in response.json()]
            return routines
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None

def getRoutineData(user_id:str, routine_id: str) -> FullRoutine | None :
    try:
        response = requests.get(
            url="http://localhost:8080/routines/data",
            params={"user_id": user_id, "routine_id": routine_id}
        )

        if response.status_code == 200:
            routine = FullRoutine(**response.json())
            routine.exercises = [RoutineExercise(**exercise) for exercise in routine.exercises]
            return routine

        else:
            print(f"Error: {response.status_code} — {response.text}")
            return None

    except Exception as e:
        print(f"Exception while fetching routine: {e}")
        return None

def getWorkoutSessionData(email_id: str) -> Workout | None :
    return