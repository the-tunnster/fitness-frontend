from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    gender: str
    dateOfBirth: str
    height: float
    weight: float
    unitPreference: str
    id: Optional[str]
