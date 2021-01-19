def interleave(*iterables):
    for elements in zip(*iterables):
        for element in elements:
            yield element