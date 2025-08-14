from dataclasses import dataclass

@dataclass
class FullUser:
    id: str
    email: str
    gender: str
    username: str
    height: float
    weight: float
    dateOfBirth: str
    unitPreference: str
    clearanceLevel: int
    stravaAccessToken: str
    stravaRefreshToken: str

@dataclass
class BasicUser:
    id: str
    username: str
    clearanceLevel: int
