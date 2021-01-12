
def validate(*ls):
    if not all([type()])

def add(*ls):
    rv = [[sum(items) for items in zip(*sublists)] for sublists in zip(*ls)]
    return rv


if __name__ == '__main__':
    rv = add([[5]], [[-2]])
    print(rv)
