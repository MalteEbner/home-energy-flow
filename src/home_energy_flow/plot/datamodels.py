from pydantic import BaseModel


class MonthlyData(BaseModel):
    name: str
    data: list[float]
