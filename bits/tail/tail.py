
def tail(seq, idxs):
    if idxs <= 0:
        return []
    seq = list(seq)
    return list(reversed(seq[:-idxs-1:-1]))


if __name__ == '__main__':
    print(tail([1, 2], 1))
