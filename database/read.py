import requests
import streamlit
from typing import Any

from config.urls import *

from models.user import User
from models.session import *
from models.routines import *
from models.exercise import Exercise

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

def getRoutinesList(user_id: str | None) -> list[Routine] | None :
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

def getRoutineData(user_id:str | None, routine_id: str | None) -> FullRoutine | None :
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
    
def checkWorkoutCount(user_id: str | None) -> int :
    try:
        response = requests.get(
            url=WORKOUT_URLS["count"],
            params={"user_id": user_id}
        )

        response.raise_for_status()

        return response.json()
        
    except Exception as e:
        print(f"Exception while checking for workout: {e}")
        return 0
    
def getHistoryData(user_id: str | None, exercise_id: str) -> list[dict[Any, Any]] | None :
    try:
        response = requests.get(
            url=HISTORY_URLS["data"],
            params={"user_id": user_id, "exercise_id": exercise_id}
        )

        response.raise_for_status()

        return response.json()
        
    except Exception as e:
        print(f"Exception while checking for history: {e}")
        return None