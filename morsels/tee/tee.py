import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    'logfiles', nargs='*')

parser.add_argument(
    '--append', '-a', default='w', action='store_const', const='a',
    )

args = parser.parse_args()
file_mode = args.append
binary_data = sys.stdin.buffer.read()

try:
    unicode_data = binary_data.replace(b'\r', b'').decode('utf-8')
    for logfile in args.logfiles:
        with open(logfile, file_mode) as f:
            f.write(unicode_data)
    sys.stdout.write(unicode_data)
except UnicodeError:
    for logfile in args.logfiles:
        with open(logfile, file_mode + 'b') as f:
            f.write(binary_data)
    sys.stdout.buffer.write(binary_data)
