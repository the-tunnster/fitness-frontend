from dataclasses import dataclass
from typing import List

@dataclass
class Exercise:
    name: str
    category: str
    primary_muscle: str
    secondary_muscle: str
    tertiary_muscle: str
    variations: List[str]
    equipment: List[str]
    id: str
