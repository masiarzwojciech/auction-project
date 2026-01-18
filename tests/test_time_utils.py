from datetime import timezone

from time_utils import parse_auction_datetime


def test_parse_auction_datetime_with_multiple_timezones():
    dt = parse_auction_datetime("Wed Sep 03, 3:30pm CEDT CEST")

    assert dt.tzinfo == timezone.utc
    assert dt.hour == 13  # 15:30 CEST -> 13:30 UTC
