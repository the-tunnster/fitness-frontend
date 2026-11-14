from dataclasses import dataclass

@dataclass(slots=True)
class FullUser:
    id: str
    gender: str
    username: str
    height: float
    weight: float
    date_of_birth: str
    unit_preference: str

@dataclass(slots=True)
class BasicUser:
    id: str
    username: str
