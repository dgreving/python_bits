def to_sec(s):
    things = s.split(':')
    if len(things) == 2:
        hours = 0
        minutes, seconds = things
    elif len(things) == 3:
        hours, minutes, seconds = things
    total_seconds = int(seconds) + int(minutes) * 60 + int(hours) * 3600
    return total_seconds


def sum_timestamps(lst):
    secs = sum([to_sec(x) for x in lst])
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    if not hours:
        return f'{minutes}:{seconds:02d}'
    else:
        return f'{hours}:{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    rv = sum_timestamps(['5:02', '31:06'])
    print(rv)
    #print(to_sec('01:24:15'))
