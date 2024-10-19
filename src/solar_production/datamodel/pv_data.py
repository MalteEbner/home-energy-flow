from pydantic import BaseModel, Field
from typing import List, Optional
from solar_production.datamodel.common_data import Azimuth, Slope


class Module(BaseModel):
    slope: Slope
    azimuth: Azimuth
    kWP: float = 0.5
    n: int = 1


class PVSystem(BaseModel):
    modules: List[Module]
    maximum_power_kW: float | None = None
