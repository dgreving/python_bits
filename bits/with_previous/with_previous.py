def with_previous(iterable, *, fillvalue=None):
    previous = fillvalue
    for item in iterable:
        yield (item, previous)
        previous = item
