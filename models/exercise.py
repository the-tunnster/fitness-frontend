from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Exercise:
    name: str
    category: str
    primary_muscle: str
    secondary_muscle: str
    tertiary_muscle: str
    variations: List[str]
    equipment: List[str]
    created_at: datetime
    updated_at: datetime
    id: Optional[str]
