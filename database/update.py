import requests
from dataclasses import asdict

from config.urls import *

from models.user import FullUser, BasicUser
from models.routines import FullRoutine
from models.session import WorkoutSession
from models.cardio import CardioSession
from models.exercise import Exercise

def updateUserProfile(user: FullUser, user_id: str) -> bool:
    try:
        payload = asdict(user)
        payload.pop("id")
        payload.pop("stravaAccessToken")
        payload.pop("stravaRefreshToken")

        response = requests.patch(
            url=USER_URLS["update"],
            params={"user_id": user_id},
            json=payload
        )

        if response.status_code in (200, 204):
            print(f"User profile for ID {user_id} updated successfully.")
            return True
        else:
            print(f"Error updating user profile: Status Code {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False


def updateUserRoutine(user: BasicUser, routine: FullRoutine) -> bool:
    try:
        payload = [asdict(ex) for ex in routine.exercises]

        response = requests.patch(
            url=ROUTINE_URLS["update"],
            params={"user_id": user.id, "routine_id":routine.id},
            json=payload
        )

        if response.status_code in (200, 204):  # 204 = No Content, 200 = OK
            print(f"User routine for ID {routine.id} updated successfully.")
            return True
        else:
            print(f"Error updating user routine: Status Code {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False


def updateWorkoutSession(session: WorkoutSession) -> bool:
    try:
        payload = [asdict(ex) for ex in session.exercises]

        response = requests.patch(
            url=SESSION_URLS["update"],
            params={"session_id": session.id, "exercise_index": session.exercise_index},
            json=payload
        )

        if response.status_code in (200, 204):  # 204 = No Content, 200 = OK
            print(f"User session for ID {session.id} updated successfully.")
            return True
        else:
            print(f"Error updating user session: Status Code {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False
    

def updateExerciseHistory(user_id: str | None, workout_id: str) -> bool:
    try:
        response = requests.patch(
            url=HISTORY_URLS["update"],
            params={"user_id": user_id, "workout_id": workout_id}
        )

        if response.status_code == 204:
            print("History updated successfully!")
            return True
        else:
            print(f"Error updating history files: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception during history update: {e}")
        return False
    
def updateCardioHistory(user_id: str | None, cardio_id: str, session: CardioSession) -> bool:
    try:
        payload = asdict(session)
        response = requests.patch(
            url=CARDIO_URLS["update"],
            params={"user_id": user_id, "cardio_id": cardio_id},
            json=payload
        )

        if response.status_code == 204:
            print("History updated successfully! No content returned.")
            return True
        else:
            print(f"Error updating cardio history files: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception during cardio history update: {e}")
        return False


def updateExercise(exercise: Exercise) -> bool:
    try:
        payload = asdict(exercise)
        response = requests.patch(
            url=EXERCISE_URLS["update"],
            params={"exercise_id": exercise.id},
            json=payload
        )

        if response.status_code in (200, 204):
            print(f"Exercise '{exercise.name}' updated successfully.")
            return True
        else:
            print(f"Error updating exercise: Status Code {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f"Exception during exercise update: {e}")
        return False