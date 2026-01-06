from dataclasses import dataclass

@dataclass(slots=True)
class FullUser:
    id: str
    email: str
    gender: str
    username: str
    height: float
    weight: float
    date_of_birth: str
    unit_preference: str
    clearance_level: int
    strava_access_token: str
    strava_refresh_token: str

@dataclass(slots=True)
class BasicUser:
    id: str
    username: str
    clearance_level: int
