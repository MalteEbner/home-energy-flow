from pydantic import BaseModel
from typing import List
from home_energy_flow.production.datamodels import Azimuth
from home_energy_flow.production.datamodels import Slope


class Module(BaseModel):
    slope: Slope
    azimuth: Azimuth
    kWP: float = 0.5
    n: int = 1


class PVSystem(BaseModel):
    modules: List[Module]
    maximum_power_kW: float | None = None
