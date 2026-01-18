from datetime import datetime
from enum import Enum

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass


class VehicleType(Enum):
    AUTOMOBILE = "Automobiles"
    TRUCK = "Truck"
    SUV = "SUV"
    MOTORCYCLE = "Motorcycle"
    OTHER = "Other"

    @classmethod
    def from_string(cls, value: str) -> "VehicleType":
        """Parsuje string do VehicleType, zwraca OTHER jeśli nie znaleziono."""
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return cls.OTHER


@dataclass(frozen=True)
class Vehicle:
    year: int
    make: str
    model: str
    vehicle_type: VehicleType = Field(default=VehicleType.OTHER)
    mileage: int | None = None

    @field_validator("year", mode="after")
    @classmethod
    def validate_year(cls, v: int) -> int:
        if not 1900 <= v <= 2030:
            raise ValueError(f"Year must be between 1900 and 2030, got {v}")
        return v

    @field_validator("make", "model", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty")
        return v
    
    @field_validator("mileage", mode="after")
    @classmethod
    def validate_mileage(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError(f"Mileage must be non-negative, got {v}")
        return v


@dataclass(frozen=True)
class Auction:
    stock_number: str
    branch: str
    auction_date_utc: datetime
    vehicle: Vehicle