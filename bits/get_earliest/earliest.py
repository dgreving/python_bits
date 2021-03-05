def sortable_date(formatted):
    m, d, y = formatted.split('/')
    return int(y + m + d)


def get_earliest(*dates):
    return sorted(dates, key=sortable_date)[0]
