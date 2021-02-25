from argparse import ArgumentParser
import sys

parser = ArgumentParser()

parser.add_argument('input_file', nargs='?', default='-')
parser.add_argument('--output', '-o', default=None)
parser.add_argument('--from-code', '-f', default=sys.getdefaultencoding())
parser.add_argument('--to-code', '-t', default=sys.getdefaultencoding())
parser.add_argument('-c', default='strict', const='ignore', action='store_const')

args = parser.parse_args()


def recode(bytes_):
    return bytes_.decode(args.from_code, errors=args.c).encode(args.to_code)


if args.input_file == '-':
    data = recode(sys.stdin.buffer.read())
else:
    with open(args.input_file, 'rb') as f:
        data = recode(f.read())


if args.output:
    with open(args.output, 'wb') as o:
        o.write(data)
else:
    sys.stdout.buffer.write(data)
