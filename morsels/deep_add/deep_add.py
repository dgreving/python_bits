from _collections_abc import Iterable


def deep_add(x, start=0):
    if not isinstance(x, Iterable):
        return x
    else:
        zero = start - start
        return sum((deep_add(unit, start=zero) for unit in x), start=start)


if __name__ == '__main__':
    l = [[5, 6], 2, 3, 4]
    print(deep_add(l))
