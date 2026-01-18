from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dateutil import parser


TZINFOS = {
    "CST": ZoneInfo("America/Chicago"),
    "CDT": ZoneInfo("America/Chicago"),
    "EST": ZoneInfo("America/New_York"),
    "EDT": ZoneInfo("America/New_York"),
    "CEST": ZoneInfo("Europe/Warsaw"),
    "CEDT": ZoneInfo("Europe/Warsaw"),
}


LOCAL_TZ = ZoneInfo("Europe/Warsaw")


def _normalize_timezone_tokens(value: str) -> str:
    tokens = value.split()
    known_tz = [t for t in tokens if t in TZINFOS]

    if known_tz:
        # usuwamy wszystkie znane TZ i dokÅ‚adamy ostatniÄ…
        tokens = [t for t in tokens if t not in TZINFOS]
        tokens.append(known_tz[-1])

    return " ".join(tokens)


def parse_auction_datetime(value: str) -> datetime:
    cleaned = _normalize_timezone_tokens(value)

    dt = parser.parse(cleaned, tzinfos=TZINFOS)

    if dt.tzinfo is None:
        raise ValueError(f"Nieznana lub brak strefy czasowej: {value}")

    return dt.astimezone(timezone.utc)


def to_local_time(dt_utc: datetime) -> datetime:
    return dt_utc.astimezone(LOCAL_TZ)
