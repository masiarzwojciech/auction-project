import csv
import re
from pathlib import Path

from models import Auction, Vehicle, VehicleType
from time_utils import parse_auction_datetime


class CsvAuctionParser:
    @staticmethod
    def _parse_year(year_str: str) -> int:
        """Parsuje rok - konwertuje dwucyfrowe lata na czterocyfrowe.
        
        Konwencja:
        - 00-30 → 2000-2030
        - 31-99 → 1931-1999
        """
        year = int(year_str)
        
        if year < 100:  # Dwucyfrowy rok
            if year <= 30:
                return 2000 + year  # 00-30 → 2000-2030
            else:
                return 1900 + year  # 31-99 → 1931-1999
        
        return year  # Już czterocyfrowy
    
    @staticmethod
    def _parse_mileage(odometer_str: str) -> int | None:
        """Parsuje string odometru np. '162,022 mi' na int."""
        if not odometer_str:
            return None
        # Wyciągamy cyfry z formatu "162,022 mi"
        match = re.search(r"[\d,]+", odometer_str)
        if match:
            return int(match.group().replace(",", ""))
        return None

    @staticmethod
    def parse_row(row: dict) -> Auction:
        return Auction(
            stock_number=str(row["Stock Number"]),
            branch=row["Branch Name"],
            auction_date_utc=parse_auction_datetime(row["Auction Date"]),
            vehicle=Vehicle(
                year=CsvAuctionParser._parse_year(row["Year"]),
                make=row["Make"],
                model=row["Model"],
                vehicle_type=VehicleType.from_string(row.get("Vehicle Type", "Other")),
                mileage=CsvAuctionParser._parse_mileage(row.get("Odometer", "")),
            ),
        )

    def parse_file(self, path: Path) -> list[Auction]:
        with path.open(encoding="utf-8-sig") as f:
            return [self.parse_row(r) for r in csv.DictReader(f)]