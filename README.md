🚗 Auction Project - System Analizy Aukcji Samochodów
System do przetwarzania i analizy danych z aukcji samochodów w USA.

📋 Opis Projektu
Projekt realizuje zaawansowane przetwarzanie danych CSV z aukcji samochodów, oferując:
- Wielowątkowe ładowanie danych
- Walidację z użyciem Pydantic
- Kompleksową analizę statystyczną
- Poprawną obsługę stref czasowych
- Typowanie zgodne z PEP 484

🏗️ Struktura Projektu
auction_project/
├── data/                    # Pliki CSV z danymi aukcji
├── src/                     # Kod źródłowy
│   ├── models.py           # Modele danych (Pydantic)
│   ├── parser.py           # Parser plików CSV
│   ├── loader.py           # Wielowątkowe ładowanie danych
│   ├── service.py          # Logika biznesowa i analiza
│   ├── time_utils.py       # Obsługa stref czasowych
│   └── main.py             # Główny skrypt aplikacji
├── tests/                   # Testy jednostkowe
│   ├── test_models.py
│   ├── test_parser.py
│   ├── test_service.py
│   └── test_time_utils.py
├── requirements.txt         # Zależności projektu
└── pytest.ini              # Konfiguracja pytest
