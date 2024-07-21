def check_season(day: int) -> bool:
    month = day // 30 + 1
    if month == 1:
        return 1 <= day <= 10
    elif month == 2:
        return 21 <= day <= 29
    elif month == 3:
        return 11 <= day <= 20
    elif month == 4:
        return 1 <= day <= 20
    elif month == 5:
        return 1 <= day <= 10
    elif month == 7:
        return 1 <= day <= 20
    elif month == 8:
        return 1 <= day <= 20
    elif month == 11:
        return 21 <= day <= 30
    elif month == 12:
        return 1 <= day <= 20