from datetime import date, timedelta


class Weekday:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def meetup_date(y, m, nth=4, weekday=3):
    if nth > 0:
        dt = date(y, m, 1)
    else:
        dt = date(y, (m + 1) % 12, 1) - timedelta(days=1)
    while dt.weekday() != weekday:
        if nth > 0:
            dt += timedelta(days=1)
        else:
            dt -= timedelta(days=1)
    if nth > 0:
        return dt + timedelta(weeks=nth-1)
    else:
        return dt + timedelta(weeks=nth+1)


if __name__ == '__main__':
    rv = meetup_date(2007, 7, nth=-1)
    print(rv.weekday())
    print(Weekday.MONDAY)
