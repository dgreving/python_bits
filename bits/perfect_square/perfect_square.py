from decimal import Decimal
import cmath


def is_perfect_square(num, *, complex=False):
    if isinstance(num, str):
        raise TypeError('')
    elif not complex and num < 0:
        return False
    if complex is False:
        return int(Decimal(num).sqrt()) ** 2 == num
    elif complex is True:
        sq = cmath.sqrt(num)
        real, imag = sq.real, sq.imag
        return real.is_integer() and imag.is_integer()
