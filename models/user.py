from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    gender: str
    dateOfBirth: str
    height: float
    weight: float
    unitPreference: str
    clearanceLevel: int
    id: str
