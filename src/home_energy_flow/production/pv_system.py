from pydantic import BaseModel
from typing import List
from home_energy_flow.production.datamodels import Azimuth
from home_energy_flow.production.datamodels import Slope


class Modules(BaseModel):
    slope: Slope
    azimuth: Azimuth
    kWP: float = 0.5
    n: int = 1


class PVSystem(BaseModel):
    modules: List[Modules]
    maximum_power_kW: float | None = None
    performance_ratio: float = 0.8
