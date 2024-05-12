def format_month(month) -> str:
    if int(month) < 10:
        return f"0{month}"
    return str(month)


def format_day(day) -> str:
    if int(day) < 10:
        return f"0{day}"
    return str(day)
