from typing import Optional

from typing_extensions import Literal, overload

from .operator import InvertibleOperator, StandaloneOperator


class PointRadiusOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    @overload
    def __init__(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: int,
        radius_mi: Literal[None] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Literal[None] = None,
        radius_mi: int,
    ):
        ...

    def __init__(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Optional[int] = None,
        radius_mi: Optional[int] = None,
    ):
        self.longitude_deg = longitude_deg
        self.latitude_deg = latitude_deg

        if radius_km is not None:
            self.radius = radius_km
            self.radius_unit = "km"

        elif radius_mi is not None:
            self.radius = radius_mi
            self.radius_unit = "mi"

        else:
            self.radius = 1
            self.radius_unit = "km"

    def __str__(self) -> str:
        return f"point_radius:[{self.longitude_deg} {self.latitude_deg} {self.radius}{self.radius_unit}]"
