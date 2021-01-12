import sys
import argparse
import secrets
import math


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def my_func():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'words_fname',
        help='name of the words file',
        )

    parser.add_argument(
        "-w", "--words",
        default=4, type=int,
        help="used number of words",
        )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='toggle verbose mode',
        )

    args = parser.parse_args()

    with open(args.words_fname, 'r') as f:
        all_words = [w.strip() for w in f.readlines()]

    rv = r' '.join([secrets.choice(all_words) for _ in range(args.words)])

    entropy = round(math.log2(len(all_words)**args.words))
    equiv = round(entropy / math.log2(26*2 + 10))
    verb = (
        f'This {args.words}-word passphrase picked from {len(all_words)} words'
        f' is similar to a {equiv} character password (entropy {entropy})'
        )

    if args.verbose:
        print(rv)
        eprint(verb)
    else:
        print(rv)


if __name__ == '__main__':
    my_func()
