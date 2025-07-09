import requests
import streamlit

from config.urls import *

from models.user import *
from models.routines import *
from models.exercise import *
from models.session import *

def getUser(emailID: str) -> User | None :
    try:
        response = requests.get(
            url=USER_URLS["me"],
            params={"email": emailID}
        )

        response.raise_for_status()

        if response.json()["id"] == "000000000000000000000000":
            return None
        
        user = User(**response.json())
        return user

    except:
        return None
    
def getExerciseData(exerciseID: str) -> Exercise | None:
    try:
        response = requests.get(
            url=EXERCISE_URLS["data"],
            params={"exercise_id": exerciseID}
        )

        response.raise_for_status()

        if response.json()["id"] == "000000000000000000000000":
            return None
        
        exercise = Exercise(**response.json())
        return exercise

    except:
        return None
    
@streamlit.cache_data
def getExerciseList() -> list[Exercise] | None :
    try:
        response = requests.get(
            url=EXERCISE_URLS["list"]
        )
        
        response.raise_for_status()

        exercises = [Exercise(**item) for item in response.json()]
        return exercises

    except Exception as e:
        print(f"Exception: {e}")
        return None
    
def getExerciseNames(exercise_ids: list[str]) -> list[str] :
    try:
        response = requests.get(
            url=EXERCISE_URLS["name"],
            params=[("exercise_id", eid) for eid in exercise_ids]
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(f"Exception: {e}")
        return []

def getExerciseIDs(exercise_names: list[str]) -> list[str]:
    try:
        response = requests.get(
            url=EXERCISE_URLS["id"],
            params=[("exercise_name", name) for name in exercise_names]
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(f"Exception: {e}")
        return []

def getRoutinesList(user_id: str) -> list[Routine] | None :
    try:
        response = requests.get(
            url=ROUTINE_URLS["list"],
            params={"user_id": user_id}
        )

        response.raise_for_status()

        routines = [Routine(**item) for item in response.json()]
        return routines

    except Exception as e:
        print(f"Exception: {e}")
        return None

def getRoutineData(user_id:str, routine_id: str) -> FullRoutine | None :
    try:
        response = requests.get(
            url=ROUTINE_URLS["data"],
            params={"user_id": user_id, "routine_id": routine_id}
        )

        json_data = response.json()
        exercises = json_data.get("exercises", [])

        response.raise_for_status()

        routine = FullRoutine(**json_data)
        routine.exercises = [RoutineExercise(**exercise) for exercise in exercises]

        return routine

    except Exception as e:
        print(f"Exception while fetching routine: {e}")
        return None

def getWorkoutSessionData(user_id: str | None) -> WorkoutSession | None :
    try:
        response = requests.get(
            url=SESSION_URLS["data"],
            params={"user_id": user_id}
        )

        response.raise_for_status()

        if response.json()["id"] == "000000000000000000000000":
            return None

        json_data = response.json()
        exercises = json_data.get("exercises", [])

        session = WorkoutSession(**json_data)
        session.exercises = [WorkoutExercise(**exercise) for exercise in exercises]

        for exercise in session.exercises:
            exercise.sets = [WorkoutSet(**ws) for ws in exercise.sets] # type: ignore

        return session

    except Exception as e:
        print(f"Exception while fetching routine: {e}")
        return None
    
def checkHistoryData(user_id: str | None) -> bool | None :
    try:
        response = requests.get(
            url=HISTORY_URLS["check"],
            params={"user_id": user_id}
        )

        response.raise_for_status()

        if response.json() is True:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Exception while checking for history: {e}")
        return None
    
def getHistoryData(user_id: str, exercise_id:str) -> ExerciseHistory | None :
    try:
        response = requests.get(
            url=HISTORY_URLS["data"],
            params={"user_id": user_id, "exercise_id": exercise_id}
        )

        response.raise_for_status()

        json_data = response.json()
        exercise_sets = json_data.get("exercise_sets", [])

        exercise_history = ExerciseHistory(**json_data)
        exercise_history.exercise_sets = [ExerciseSets(**exercise_set) for exercise_set in exercise_sets]

        for exercise_set in exercise_history.exercise_sets:
            exercise_set.sets = [WorkoutSet(**ws) for ws in exercise_set.sets] # type: ignore

        return exercise_history
        
    except Exception as e:
        print(f"Exception while checking for history: {e}")
        return None