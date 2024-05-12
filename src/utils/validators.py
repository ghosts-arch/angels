def is_valid_day(day: str) -> bool:
    if 1 <= int(day) <= 31:
        return True
    return False


def is_valid_month(month: str) -> bool:
    if 1 <= int(month) <= 12:
        return True
    return False


def is_valid_year(year: str) -> bool:
    if 1970 <= int(year) <= 2024:
        return True
    return False
