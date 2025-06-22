import requests
import json
from dataclasses import asdict

from models.user import User
from models.routines import FullRoutine

def updateUserProfile(user: User, user_id: str) -> bool:
    try:
        response = requests.patch(
            url=f"http://localhost:8080/user/update?user_id={user_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(asdict(user))
        )

        if response.status_code in (200, 204):  # 204 = No Content, 200 = OK
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False


def updateUserRoutine(user: User, routine: FullRoutine) -> bool:
    try:
        response = requests.patch(
            url=f"http://localhost:8080/routines/update?user_id={user.id}&routine_id={routine.id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(asdict(routine))
        )

        if response.status_code in (200, 204):  # 204 = No Content, 200 = OK
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False