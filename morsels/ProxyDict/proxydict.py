class ProxyDict(dict):
    def __setitem__(self, idx, val):
        raise TypeError('Does not support item assignment.')

    def pop(self, key):
        raise TypeError('Does not support item assignment.')

    def setdefault(self, val):
        raise TypeError('Does not support item assignment.')

    def update(self, d):
        raise TypeError('Does not support item assignment.')


class ProxyDict:
    def __init__(self, d):
        self.d = d

    def __getitem__(self, key):
        return self.d[key]

    def keys(self):
        return self.d.keys()

    def __len__(self):
        return len(self.d)

    def items(self):
        return self.d.items()

    def values(self):
        return self.d.values()

    def get(self, key, default=None):
        return self.d.get(key, default)

    def __iter__(self):
        return iter(self.d)

    def __repr__(self):
        return f'ProxyDict({str(self.d)})'

    def __setitem__(self, idx, val):
        raise TypeError('Does not support item assignment.')

    def __eq__(self, other):
        return self.d == other

    def pop(self, key):
        raise TypeError('Does not support item assignment.')

    def setdefault(self, val):
        raise TypeError('Does not support item assignment.')

    def update(self, d):
        raise TypeError('Does not support item assignment.')


from collections.abc import Mapping


class ProxyDict(Mapping):
    def __init__(self, mapping):
        self._map = mapping

    def __getitem__(self, key):
        return self._map[key]

    def __len__(self):
        return self._map.__len__()

    def __iter__(self):
        yield from self._map

    def __repr__(self):
        return f'ProxyDict({str(self._map)})'

data = dict(a=1, b=2)
pd = ProxyDict(data)
