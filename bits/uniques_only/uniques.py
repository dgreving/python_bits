from collections import Counter


def uniques_only(iterable):
    try:
        counter = Counter(iterable)
    except:
        counter = None

    if counter:
        for element, key in zip(iterable, counter.keys()):
            yield element
    else:
        returned = []
        for element in iterable:
            if element not in returned:
                returned.append(element)
                yield element