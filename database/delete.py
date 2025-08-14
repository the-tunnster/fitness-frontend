import requests

from config.urls import *

def deleteRoutine(user_id: str | None, routine_id: str | None) -> bool :
    try:
        response = requests.delete(
            url=ROUTINE_URLS["delete"],
            params={"user_id":user_id, "routine_id": routine_id}
        )

        if response.status_code == 204 :
            return True
    except:
        return False
	
    return False

def deleteSession(session_id: str) -> bool :
    try:
        response = requests.delete(
            url=SESSION_URLS["delete"],
            params={"session_id":session_id}
        )

        if response.status_code == 204 :
            return True
    except:
        return False
	
    return False