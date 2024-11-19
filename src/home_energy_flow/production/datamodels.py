from pydantic import BaseModel


class Azimuth(BaseModel):
    value: float
    optimal: bool = False

    @classmethod
    def SOUTH(cls):
        return cls(value=0.0)

    @classmethod
    def EAST(cls):
        return cls(value=-90.0)

    @classmethod
    def WEST(cls):
        return cls(value=90.0)

    @classmethod
    def NORTH(cls):
        return cls(value=180.0)


class Slope(BaseModel):
    value: float
    optimal: bool = False
