from datetime import datetime, timezone

import pytest

from models import Auction, Vehicle, VehicleType
from service import AuctionService


@pytest.fixture
def sample_auctions() -> list[Auction]:
    return [
        Auction(
            stock_number="1",
            branch="Chicago",
            auction_date_utc=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            vehicle=Vehicle(
                year=2015,
                make="Ford",
                model="Focus",
                vehicle_type=VehicleType.AUTOMOBILE,
                mileage=120_000,
            ),
        ),
        Auction(
            stock_number="2",
            branch="Dallas",
            auction_date_utc=datetime(2024, 6, 20, 14, 0, tzinfo=timezone.utc),
            vehicle=Vehicle(
                year=2021,
                make="Toyota",
                model="Corolla",
                vehicle_type=VehicleType.AUTOMOBILE,
                mileage=40_000,
            ),
        ),
        Auction(
            stock_number="3",
            branch="Chicago",
            auction_date_utc=datetime(2024, 9, 10, 9, 0, tzinfo=timezone.utc),
            vehicle=Vehicle(
                year=2018,
                make="Ford",
                model="F-150",
                vehicle_type=VehicleType.TRUCK,
                mileage=80_000,
            ),
        ),
        Auction(
            stock_number="4",
            branch="New York",
            auction_date_utc=datetime(2024, 12, 1, 11, 0, tzinfo=timezone.utc),
            vehicle=Vehicle(
                year=2020,
                make="Honda",
                model="Civic",
                vehicle_type=VehicleType.AUTOMOBILE,
                mileage=None,
            ),
        ),
    ]


def test_filter_by_year(sample_auctions):
    result = AuctionService.filter_by_year(sample_auctions, 2018)
    assert len(result) == 3
    assert all(a.vehicle.year >= 2018 for a in result)


def test_filter_by_year_with_range(sample_auctions):
    result = AuctionService.filter_by_year(sample_auctions, 2018, 2020)
    assert len(result) == 2
    assert all(2018 <= a.vehicle.year <= 2020 for a in result)


def test_filter_by_make(sample_auctions):
    result = AuctionService.filter_by_make(sample_auctions, ["Ford"])
    assert len(result) == 2
    assert all(a.vehicle.make == "Ford" for a in result)


def test_filter_by_make_case_insensitive(sample_auctions):
    result = AuctionService.filter_by_make(sample_auctions, ["ford"])
    assert len(result) == 2


def test_filter_by_vehicle_type(sample_auctions):
    result = AuctionService.filter_by_vehicle_type(sample_auctions, VehicleType.AUTOMOBILE)
    assert len(result) == 3
    assert all(a.vehicle.vehicle_type == VehicleType.AUTOMOBILE for a in result)


def test_filter_by_date_range(sample_auctions):
    start = datetime(2024, 6, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)
    result = AuctionService.filter_by_date_range(sample_auctions, start, end)
    assert len(result) == 3


def test_group_by_make(sample_auctions):
    result = AuctionService.group_by_make(sample_auctions)
    assert len(result) == 3
    assert len(result["Ford"]) == 2
    assert len(result["Toyota"]) == 1
    assert len(result["Honda"]) == 1


def test_group_by_branch(sample_auctions):
    result = AuctionService.group_by_branch(sample_auctions)
    assert len(result) == 3
    assert len(result["Chicago"]) == 2


def test_group_by_vehicle_type(sample_auctions):
    result = AuctionService.group_by_vehicle_type(sample_auctions)
    assert len(result) == 2
    assert len(result[VehicleType.AUTOMOBILE]) == 3
    assert len(result[VehicleType.TRUCK]) == 1


def test_get_top_makes(sample_auctions):
    result = AuctionService.get_top_makes(sample_auctions, 2)
    assert len(result) == 2
    assert result[0][0] == "Ford"
    assert result[0][1] == 2


def test_get_top_models(sample_auctions):
    result = AuctionService.get_top_models(sample_auctions, 5)
    assert len(result) == 4
    assert all(count == 1 for _, count in result)


def test_get_average_mileage_by_year(sample_auctions):
    result = AuctionService.get_average_mileage_by_year(sample_auctions)
    assert result[2015] == 120_000
    assert result[2021] == 40_000
    assert result[2018] == 80_000
    assert 2020 not in result  # brak danych o przebiegu


def test_get_statistics(sample_auctions):
    stats = AuctionService.get_statistics(sample_auctions)
    assert stats["total_auctions"] == 4
    assert stats["unique_makes"] == 3
    assert stats["unique_branches"] == 3
    assert stats["year_range"] == (2015, 2021)
    assert stats["avg_mileage"] == 80_000  # (120k + 40k + 80k) / 3
    assert stats["median_mileage"] == 80_000
