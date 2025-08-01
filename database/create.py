import requests
from typing import Any
from dataclasses import asdict

from config.urls import *

from models.user import User
from models.exercise import Exercise
from models.routines import FullRoutine

def createDummyUserProfile(emailID: str, username: str) -> bool:
    new_user = User(
        username=username,
        email=emailID,
        gender="male",
        dateOfBirth="2000-05-21T00:00:00Z",
        height=175.0,
        weight=78.5,
        unitPreference="metric",
        clearanceLevel=1,
        id=None
    )

    try:
        response = requests.post(
            url=USER_URLS["create"],
            json=asdict(new_user)
        )

        if response.status_code == 201:
            return True
        
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False

def createUserRoutine(user: User, routine: FullRoutine) -> bool:
    try:
        payload: dict[str, Any] = {
            "name": routine.name,
            "exercises": [asdict(ex) for ex in routine.exercises]
        }

        response = requests.post(
            url=ROUTINE_URLS["create"],
            params={"user_id": user.id},
            json=payload
        )

        if response.status_code == 201:
            print(f"User routine created successfully! Routine ID: {response.json()}")
            return True
        
        else:
            print(f"Error creating routine: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception during routine creation: {e}")
        return False
    
def createWorkoutSession(user_id: str | None, routine_id: str) -> bool:
    try:
        response = requests.post(
            url=SESSION_URLS["create"],
            params={"user_id": user_id, "routine_id": routine_id}
        )

        if response.status_code == 201:
            print(f"Workout session created successfully! Session ID: {response.json()}")
            return True
        else:
            print(f"Error creating workout session: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception during workout session creation: {e}")
        return False
    
def createWorkout(session_id: str) -> str | None:
    try:
        response = requests.post(
            url=WORKOUT_URLS["create"],
            params={"session_id": session_id}
        )

        if response.status_code == 201:
            print(f"Workout saved successfully! Workout ID: {response.json()}")
            return response.json()
        else:
            print(f"Error saving workout : {response.status_code}, {response.text}")
            return None

    except Exception as e:
        print(f"Exception during workout saving: {e}")
        return None
    
def createHistory(user_id: str) -> bool:
    try:
        response = requests.post(
            url=HISTORY_URLS["create"],
            params={"user_id": user_id}
        )

        if response.status_code == 201:
            print(f"History created successfully! User ID: {response.json()}")
            return True
        else:
            print(f"Error creating history files: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception during history creation: {e}")
        return False


def createExercise(exercise: Exercise) -> str | None:
    try:
        payload = asdict(exercise)
        payload.pop('id', None)
        
        response = requests.post(
            url=EXERCISE_URLS["create"],
            json=payload
        )

        if response.status_code == 201:
            exercise_id = response.json()
            return exercise_id
        else:
            print(f"Error creating exercise: Status Code {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f"Exception during exercise creation: {e}")
        return None