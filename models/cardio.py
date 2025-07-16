from dataclasses import dataclass

@dataclass
class Cardio:
	id: str
	name: str
	variations: list[str]

@dataclass
class CardioMetric:
	total_distance: float
	total_time: float
	calories_burned: float
	heart_rate: int

@dataclass
class CardioSession:
	variation: str
	metrics: CardioMetric