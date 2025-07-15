from dataclasses import dataclass

@dataclass
class Cardio:
	id: str
	name: str
	category: str
	variations: list[str]
	equipment: list[str]

@dataclass
class CardioMetric:
	total_distance: float
	total_time: float
	distance_splits: list[float]
	time_splits: list[float]
	average_pace: float
	calories_burned: float
	heart_rate: int

@dataclass
class CardioSession:
	equipment: str
	variation: str
	metrics: CardioMetric