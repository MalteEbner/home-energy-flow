from pydantic import BaseModel


class MonthlyData(BaseModel):
    name: str
    year: int
    data: list[float]
