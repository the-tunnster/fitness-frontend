import requests
from dataclasses import asdict

from config.urls import *

from models.user import User
from models.routines import FullRoutine

def updateUserProfile(user: User, user_id: str) -> bool:
    try:
        response = requests.patch(
            url=USER_URLS["update"],
            params={"user_id": user_id},
            json=asdict(user)
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


def updateUserRoutine(user: User, routine: FullRoutine) -> bool:
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