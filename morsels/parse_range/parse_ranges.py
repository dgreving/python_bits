def handle_unit(u):
    if '->' in u:
        return [int(u.split('->')[0])]
    elif '-' in u:
        start, end = u.split('-')
        return range(int(start), int(end)+1)
    else:
        return [int(u)]


def parse_ranges(s):
    for unit in s.replace(' ', '').split(','):
        for num in handle_unit(unit):
            yield num
