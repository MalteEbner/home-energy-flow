import re
from pydantic import BaseModel, Field
from typing import Optional

from home_energy_flow.production.datamodels import Azimuth
from home_energy_flow.production.datamodels import Slope


class Location(BaseModel):
    latitude: float
    longitude: float
    elevation: float


class MeteoData(BaseModel):
    radiation_db: str
    meteo_db: str
    year_min: int
    year_max: int
    use_horizon: bool
    horizon_db: str | None = None
    horizon_data: str


class FixedMountingSystem(BaseModel):
    slope: Slope
    azimuth: Azimuth
    type: str


class MountingSystem(BaseModel):
    fixed: FixedMountingSystem


class PvModule(BaseModel):
    technology: Optional[str] = None
    peak_power: Optional[float] = None
    system_loss: Optional[float] = None


class Time(BaseModel):
    year: int
    month: int
    day: int
    hour: int

    @classmethod
    def from_string(cls, time_str: str) -> "Time":
        # Parse time in format 'YYYYMMDD:HHMM'
        match = re.match(r"(\d{4})(\d{2})(\d{2}):(\d{2})(\d{2})", time_str)
        if match:
            year, month, day, hour, minute = map(int, match.groups())
            return cls(year=year, month=month, day=day, hour=hour)
        else:
            raise ValueError(f"Invalid time format: {time_str}")


class TimeSeriesEntry(BaseModel):
    time: Time
    G_i: float = Field(..., alias="G(i)")
    H_sun: float
    T2m: float
    WS10m: float
    Int: float

    @classmethod
    def from_dict(cls, data: dict) -> "TimeSeriesEntry":
        # Convert the 'time' field from string to Time instance
        time = Time.from_string(data["time"])
        return cls(
            time=time,
            G_i=data["G(i)"],
            H_sun=data["H_sun"],
            T2m=data["T2m"],
            WS10m=data["WS10m"],
            Int=data["Int"],
        )


class Inputs(BaseModel):
    location: Location
    meteo_data: MeteoData
    mounting_system: MountingSystem
    pv_module: PvModule


class Outputs(BaseModel):
    hourly: list[TimeSeriesEntry]


class SolarRadiationData(BaseModel):
    inputs: Inputs
    outputs: Outputs
