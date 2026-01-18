import pytest

from models import VehicleType
from parser import CsvAuctionParser


def test_parse_mileage_standard():
    """Test parsowania standardowego formatu odometru."""
    assert CsvAuctionParser._parse_mileage("162,022 mi") == 162_022


def test_parse_mileage_without_comma():
    """Test parsowania odometru bez przecinka."""
    assert CsvAuctionParser._parse_mileage("5000 mi") == 5000


def test_parse_mileage_large_number():
    """Test parsowania dużych liczb."""
    assert CsvAuctionParser._parse_mileage("1,234,567 mi") == 1_234_567


def test_parse_mileage_empty_string():
    """Test parsowania pustego stringa."""
    assert CsvAuctionParser._parse_mileage("") is None


def test_parse_mileage_none():
    """Test obsługi None."""
    assert CsvAuctionParser._parse_mileage("") is None


def test_parse_year_four_digit():
    """Test parsowania czterocyfrowego roku."""
    assert CsvAuctionParser._parse_year("2020") == 2020
    assert CsvAuctionParser._parse_year("1995") == 1995


def test_parse_year_two_digit_2000s():
    """Test parsowania dwucyfrowego roku (2000-2030)."""
    assert CsvAuctionParser._parse_year("15") == 2015
    assert CsvAuctionParser._parse_year("20") == 2020
    assert CsvAuctionParser._parse_year("00") == 2000
    assert CsvAuctionParser._parse_year("30") == 2030


def test_parse_year_two_digit_1900s():
    """Test parsowania dwucyfrowego roku (1931-1999)."""
    assert CsvAuctionParser._parse_year("95") == 1995
    assert CsvAuctionParser._parse_year("85") == 1985
    assert CsvAuctionParser._parse_year("99") == 1999
    assert CsvAuctionParser._parse_year("31") == 1931


def test_parse_row_complete_data():
    """Test parsowania kompletnego wiersza."""
    row = {
        "Stock Number": "12345",
        "Branch Name": "Chicago",
        "Auction Date": "Mon Mar 04, 8:30am CST",
        "Year": "2020",
        "Make": "Toyota",
        "Model": "Camry",
        "Vehicle Type": "Automobiles",
        "Odometer": "50,000 mi",
    }
    
    auction = CsvAuctionParser.parse_row(row)
    
    assert auction.stock_number == "12345"
    assert auction.branch == "Chicago"
    assert auction.vehicle.year == 2020
    assert auction.vehicle.make == "Toyota"
    assert auction.vehicle.model == "Camry"
    assert auction.vehicle.vehicle_type == VehicleType.AUTOMOBILE
    assert auction.vehicle.mileage == 50_000


def test_parse_row_missing_mileage():
    """Test parsowania wiersza bez danych o przebiegu."""
    row = {
        "Stock Number": "12345",
        "Branch Name": "Dallas",
        "Auction Date": "Wed Sep 03, 3:30pm CEDT",
        "Year": "2018",
        "Make": "Ford",
        "Model": "F-150",
        "Vehicle Type": "Truck",
        "Odometer": "",
    }
    
    auction = CsvAuctionParser.parse_row(row)
    assert auction.vehicle.mileage is None


def test_parse_row_unknown_vehicle_type():
    """Test parsowania wiersza z nieznanym typem pojazdu."""
    row = {
        "Stock Number": "12345",
        "Branch Name": "New York",
        "Auction Date": "Mon Mar 04, 8:30am EST",
        "Year": "2019",
        "Make": "Tesla",
        "Model": "Model 3",
        "Vehicle Type": "Electric Vehicle",
        "Odometer": "30,000 mi",
    }
    
    auction = CsvAuctionParser.parse_row(row)
    assert auction.vehicle.vehicle_type == VehicleType.OTHER


def test_parse_row_two_digit_year():
    """Test parsowania wiersza z dwucyfrowym rokiem."""
    row = {
        "Stock Number": "12345",
        "Branch Name": "Chicago",
        "Auction Date": "Mon Mar 04, 8:30am CST",
        "Year": "15",  # Powinno być przekonwertowane na 2015
        "Make": "Honda",
        "Model": "Civic",
        "Vehicle Type": "Automobiles",
        "Odometer": "80,000 mi",
    }
    
    auction = CsvAuctionParser.parse_row(row)
    assert auction.vehicle.year == 2015