import requests

from models.user import *
from models.routines import *
from models.exercise import *

def deleteRoutine(user_id:str, routine_id: str) -> bool :
    try:
        response = requests.request(
            method="GET",
            url="http://localhost:8080/routines/delete",
            params={"user_id":user_id, "routine_id": routine_id}
        )

        if response.status_code == 204 :
            return True
    except:
        return False
	
    return False