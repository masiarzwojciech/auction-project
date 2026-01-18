from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from models import Auction, Vehicle, VehicleType


def test_vehicle_valid():
    """Test tworzenia poprawnego pojazdu."""
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        vehicle_type=VehicleType.AUTOMOBILE,
        mileage=50_000,
    )
    assert vehicle.year == 2020
    assert vehicle.make == "Toyota"


def test_vehicle_invalid_year_too_low():
    """Test walidacji - rok zbyt niski."""
    with pytest.raises(ValidationError):
        Vehicle(
            year=1800,
            make="Oldsmobile",
            model="Curved Dash",
            vehicle_type=VehicleType.AUTOMOBILE,
        )


def test_vehicle_invalid_year_too_high():
    """Test walidacji - rok zbyt wysoki."""
    with pytest.raises(ValidationError):
        Vehicle(
            year=2050,
            make="Tesla",
            model="Cybertruck",
            vehicle_type=VehicleType.AUTOMOBILE,
        )


def test_vehicle_invalid_empty_make():
    """Test walidacji - pusta marka."""
    with pytest.raises(ValidationError):
        Vehicle(
            year=2020,
            make="",
            model="Camry",
            vehicle_type=VehicleType.AUTOMOBILE,
        )


def test_vehicle_invalid_negative_mileage():
    """Test walidacji - ujemny przebieg."""
    with pytest.raises(ValidationError):
        Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleType.AUTOMOBILE,
            mileage=-1000,
        )


def test_vehicle_whitespace_trimming():
    """Test przycinania białych znaków."""
    vehicle = Vehicle(
        year=2020,
        make="  Toyota  ",
        model="  Camry  ",
        vehicle_type=VehicleType.AUTOMOBILE,
    )
    assert vehicle.make == "Toyota"
    assert vehicle.model == "Camry"


def test_vehicle_frozen():
    """Test niemutowalności (frozen=True)."""
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        vehicle_type=VehicleType.AUTOMOBILE,
    )
    with pytest.raises(AttributeError):
        vehicle.make = "Honda"


def test_vehicle_type_from_string():
    """Test parsowania typu pojazdu ze stringa."""
    assert VehicleType.from_string("Automobiles") == VehicleType.AUTOMOBILE
    assert VehicleType.from_string("automobiles") == VehicleType.AUTOMOBILE
    assert VehicleType.from_string("TRUCK") == VehicleType.TRUCK
    assert VehicleType.from_string("Unknown") == VehicleType.OTHER


def test_vehicle_default_type():
    """Test domyślnej wartości vehicle_type."""
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
    )
    assert vehicle.vehicle_type == VehicleType.OTHER


def test_auction_valid():
    """Test tworzenia poprawnej aukcji."""
    auction = Auction(
        stock_number="12345",
        branch="Chicago",
        auction_date_utc=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
        vehicle=Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleType.AUTOMOBILE,
        ),
    )
    assert auction.stock_number == "12345"
    assert auction.branch == "Chicago"


def test_auction_frozen():
    """Test niemutowalności aukcji."""
    auction = Auction(
        stock_number="12345",
        branch="Chicago",
        auction_date_utc=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
        vehicle=Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleType.AUTOMOBILE,
        ),
    )
    with pytest.raises(AttributeError):
        auction.branch = "Dallas"