from datetime import date, timedelta


def meetup_date(y, m, nth=4, weekday=3):
    dt = date(y, m, 1)
    while dt.weekday() != weekday:
        dt += timedelta(days=1)
    return dt + timedelta(weeks=nth-1)


if __name__ == '__main__':
    rv = meetup_date(2007, 7)
    print(rv.weekday())
