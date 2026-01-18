from pathlib import Path

from loader import AuctionLoader
from parser import CsvAuctionParser
from service import AuctionService
from time_utils import to_local_time


def main() -> None:
    # Wczytanie wszystkich plików CSV
    # Sprawdź czy jesteśmy w src/ czy w głównym katalogu
    data_dir = Path("../data") if Path("../data").exists() else Path("data")
    paths = list(data_dir.glob("*.csv"))
    print(f"Znaleziono {len(paths)} plików CSV\n")

    # Załadowanie danych z użyciem multithreading
    auctions = AuctionLoader(CsvAuctionParser()).load(paths)
    print(f"Wczytano {len(auctions)} aukcji\n")

    # Podstawowe statystyki
    stats = AuctionService.get_statistics(auctions)
    print("=== STATYSTYKI ===")
    print(f"Liczba aukcji: {stats['total_auctions']}")
    print(f"Unikalne marki: {stats['unique_makes']}")
    print(f"Unikalne oddziały: {stats['unique_branches']}")
    print(f"Zakres lat: {stats['year_range'][0]}-{stats['year_range'][1]}")
    print(f"Średni przebieg: {stats['avg_mileage']:.0f} mil" if stats['avg_mileage'] else "Średni przebieg: brak danych")
    print(f"Mediana przebiegu: {stats['median_mileage']:.0f} mil" if stats['median_mileage'] else "Mediana przebiegu: brak danych")
    print(f"\nTypy pojazdów:")
    for vtype, count in stats['vehicle_types'].items():
        print(f"  {vtype.value}: {count}")

    # Top 10 marek
    print("\n=== TOP 10 MAREK ===")
    for make, count in AuctionService.get_top_makes(auctions, 10):
        print(f"{make}: {count}")

    # Top 5 modeli
    print("\n=== TOP 5 MODELI ===")
    for model, count in AuctionService.get_top_models(auctions, 5):
        print(f"{model}: {count}")

    # Przykład filtrowania
    recent_cars = AuctionService.filter_by_year(auctions, 2015)
    print(f"\n=== POJAZDY Z 2015+ ===")
    print(f"Liczba: {len(recent_cars)}")

    # Przykładowa aukcja
    if auctions:
        print("\n=== PRZYKŁADOWA AUKCJA ===")
        sample = auctions[0]
        print(f"Marka: {sample.vehicle.make}")
        print(f"Model: {sample.vehicle.model}")
        print(f"Rok: {sample.vehicle.year}")
        print(f"Typ: {sample.vehicle.vehicle_type.value}")
        print(f"Przebieg: {sample.vehicle.mileage} mil" if sample.vehicle.mileage else "Przebieg: brak danych")
        print(f"Data aukcji (UTC): {sample.auction_date_utc}")
        print(f"Data aukcji (lokalna): {to_local_time(sample.auction_date_utc)}")
        print(f"Oddział: {sample.branch}")
    else:
        print("\n⚠️  Brak danych do wyświetlenia. Sprawdź czy pliki CSV są w folderze 'data/'.")


if __name__ == "__main__":
    main()