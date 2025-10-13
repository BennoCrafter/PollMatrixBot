import re
from datetime import timedelta
from typing import Optional


def parse_time(time_str: str) -> Optional[timedelta]:
    """
    Parses strings like '10s', '5m', '2h', '3d' into timedelta.
    Supports combinations like '1h30m', '2h15m10s', etc.
    """
    pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?"
    match = re.match(pattern, time_str.lower())
    if not match:
        raise ValueError("Invalid time format. Use formats like 10m, 2h30m, etc.")

    days, hours, minutes, seconds = match.groups()
    if not any([days, hours, minutes, seconds]):
        return None

    return timedelta(
        days=int(days) if days else 0,
        hours=int(hours) if hours else 0,
        minutes=int(minutes) if minutes else 0,
        seconds=int(seconds) if seconds else 0,
    )


if __name__ == "__main__":
    print(parse_time("10s"))
    print(parse_time("5m"))
    print(parse_time("2h"))
    print(parse_time("3d"))
    print(parse_time("1h30m"))
    print(parse_time("2h15m10s"))
