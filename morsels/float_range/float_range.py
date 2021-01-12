import operator
import math


class float_range:
    def __init__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            raise TypeError()
        elif len(args) > 3:
            raise TypeError()

        self.stop = kwargs.get('stop')
        if not self.stop:
            self.stop = args[0] if len(args) == 1 else args[1]

        self.step = kwargs.get('step')
        if not self.step:
            self.step = args[2] if len(args) == 3 else 1

        self.start = kwargs.get('start')
        if not self.start:
            self.start = args[0] if len(args) >= 2 else 0

    def __len__(self):
        if self.step > 0 and self.stop < self.start:
            return 0
        elif self.step < 0 and self.start < self.stop:
            return 0
        else:
            return math.ceil((self.stop - self.start) / self.step)

    def __reversed__(self):
        return reversed(list(self.__iter__()))

    def __eq__(self, other):
        if isinstance(other, range) or isinstance(other, float_range):
            if len(self) == 0 and len(other) == 0:
                return True
            if self.start == other.start and self.step > self.stop and other.step>other.stop:
                return True
            self_last = self.start + (len(self)-1) * self.step
            other_last = other.start + (len(other) - 1) * other.step
            return all([
                self.start == other.start,
                self_last == other_last,
                self.step == other.step,
            ])
        elif hasattr(other, '__eq__'):
            return other == self
        else:
            return False

    def __iter__(self):
        current = self.start
        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step
        else:
            while current > self.stop:
                yield current
                current += self.step




if __name__ == '__main__':
    print(list(float_range(0.5, 10)))
    print(len(float_range(0.5, 10)))
    
    print(list(float_range(0, 0.3, 0.5)))
    print(list(float_range(0, 0.4, 1.5)))