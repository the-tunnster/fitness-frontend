import requests
import json
from dataclasses import asdict

from models.user import User
from models.routines import FullRoutine

def createDummyUserProfile(emailID: str, username: str) -> bool:
    new_user = User(
        username=username,
        email=emailID,
        gender="male",
        dateOfBirth="2000-05-21T00:00:00Z",  # Correct format
        height=175.0,
        weight=78.5,
        unitPreference="metric",
        id=None
    )

    try:
        response = requests.post(
            url="http://localhost:8080/user/create",
            headers={"Content-Type": "application/json"},
            data=json.dumps(asdict(new_user))
        )

        if response.status_code == 201:
            return True
        
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Exception: {e}")
        return False

def createUserRoutine(user: User, routine: FullRoutine) -> bool:
    try:
        response = requests.post(
            url=f"http://localhost:8080/routines/create?user_id={user.id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(asdict(routine))
        )

        if response.status_code == 201:
            return True
        
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Exception: {e}")
        return False