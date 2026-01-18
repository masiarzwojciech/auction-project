from collections import Counter, defaultdict
from datetime import datetime
from statistics import mean, median

from models import Auction, VehicleType


class AuctionService:
    @staticmethod
    def filter_by_year(
        auctions: list[Auction],
        min_year: int,
        max_year: int | None = None,
    ) -> list[Auction]:
        """Filtruje aukcje po roku pojazdu."""
        return [
            a for a in auctions
            if a.vehicle.year >= min_year
            and (max_year is None or a.vehicle.year <= max_year)
        ]

    @staticmethod
    def filter_by_make(
        auctions: list[Auction],
        makes: list[str],
    ) -> list[Auction]:
        """Filtruje aukcje po markach (case-insensitive)."""
        makes_lower = {m.lower() for m in makes}
        return [a for a in auctions if a.vehicle.make.lower() in makes_lower]

    @staticmethod
    def filter_by_vehicle_type(
        auctions: list[Auction],
        vehicle_type: VehicleType,
    ) -> list[Auction]:
        """Filtruje aukcje po typie pojazdu."""
        return [a for a in auctions if a.vehicle.vehicle_type == vehicle_type]

    @staticmethod
    def filter_by_date_range(
        auctions: list[Auction],
        start_date: datetime,
        end_date: datetime,
    ) -> list[Auction]:
        """Filtruje aukcje po zakresie dat."""
        return [
            a for a in auctions
            if start_date <= a.auction_date_utc <= end_date
        ]

    @staticmethod
    def group_by_make(auctions: list[Auction]) -> dict[str, list[Auction]]:
        """Grupuje aukcje po markach."""
        groups: dict[str, list[Auction]] = defaultdict(list)
        for auction in auctions:
            groups[auction.vehicle.make].append(auction)
        return dict(groups)

    @staticmethod
    def group_by_branch(auctions: list[Auction]) -> dict[str, list[Auction]]:
        """Grupuje aukcje po oddziałach."""
        groups: dict[str, list[Auction]] = defaultdict(list)
        for auction in auctions:
            groups[auction.branch].append(auction)
        return dict(groups)

    @staticmethod
    def group_by_vehicle_type(auctions: list[Auction]) -> dict[VehicleType, list[Auction]]:
        """Grupuje aukcje po typach pojazdów."""
        groups: dict[VehicleType, list[Auction]] = defaultdict(list)
        for auction in auctions:
            groups[auction.vehicle.vehicle_type].append(auction)
        return dict(groups)

    @staticmethod
    def get_top_makes(auctions: list[Auction], n: int = 10) -> list[tuple[str, int]]:
        """Zwraca n najpopularniejszych marek."""
        return Counter(a.vehicle.make for a in auctions).most_common(n)

    @staticmethod
    def get_top_models(auctions: list[Auction], n: int = 10) -> list[tuple[str, int]]:
        """Zwraca n najpopularniejszych modeli."""
        return Counter(
            f"{a.vehicle.make} {a.vehicle.model}" for a in auctions
        ).most_common(n)

    @staticmethod
    def get_average_mileage_by_year(auctions: list[Auction]) -> dict[int, float]:
        """Oblicza średni przebieg dla każdego rocznika."""
        year_mileages: dict[int, list[int]] = defaultdict(list)
        
        for auction in auctions:
            if auction.vehicle.mileage is not None:
                year_mileages[auction.vehicle.year].append(auction.vehicle.mileage)
        
        return {
            year: mean(mileages)
            for year, mileages in year_mileages.items()
        }

    @staticmethod
    def get_statistics(auctions: list[Auction]) -> dict:
        """Zwraca podstawowe statystyki o aukcjach."""
        mileages = [a.vehicle.mileage for a in auctions if a.vehicle.mileage is not None]
        years = [a.vehicle.year for a in auctions]
        
        return {
            "total_auctions": len(auctions),
            "unique_makes": len(set(a.vehicle.make for a in auctions)),
            "unique_branches": len(set(a.branch for a in auctions)),
            "year_range": (min(years), max(years)) if years else (None, None),
            "avg_mileage": mean(mileages) if mileages else None,
            "median_mileage": median(mileages) if mileages else None,
            "vehicle_types": dict(Counter(a.vehicle.vehicle_type for a in auctions)),
        }
