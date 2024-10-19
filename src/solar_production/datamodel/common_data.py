from pydantic import BaseModel


class Azimuth(BaseModel):
    value: float
    optimal: bool = False


class Slope(BaseModel):
    value: float
    optimal: bool = False


class MonthlyData(BaseModel):
    name: str
    data: list[float]
