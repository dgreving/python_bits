from argparse import ArgumentParser
import re
from sys import getsizeof


parser = ArgumentParser()
parser.add_argument('searchfor', type=str)
parser.add_argument('fnames',  type=str, nargs='+')
parser.add_argument(
    '--ignore-case', '-i',
    default=False, const=True,
    action='store_const',
)
parser.add_argument(
    '--line-number', '-n',
    default=False, const=True,
    action='store_const',
)
parser.add_argument(
    '--invert-match', '-v',
    default=False, const=True,
    action='store_const',
)
parser.add_argument(
    '--initial-tab', '-T',
    default=False, const=True,
    action='store_const',
)
args = parser.parse_args()


prefix_filenames = len(args.fnames) != 1
prefix_linenumbers = args.line_number
print_tabs = args.initial_tab


def toggle(searchfor, line, invert):
    if args.ignore_case:
        search_for, line = searchfor.lower(), line.lower()
    if not invert:
        return bool(re.search(searchfor, line))
    else:
        return not bool(re.search(searchfor, line))


def print_line(line, filename, linenumber):
    fname_prefix = f'{filename}:' if prefix_filenames else ''
    pad = len(str(getsizeof(file)))
    if print_tabs:
        linenumber_prefix = f'{linenumber:{pad}}:' if prefix_linenumbers else ''
    else:
        linenumber_prefix = f'{linenumber}:' if prefix_linenumbers else ''
    spacing = '\t' if print_tabs else ''
    print(fname_prefix + linenumber_prefix + spacing + line, end='')


files = []
for fname in args.fnames:
    with open(fname, 'r') as f:
        files.append(f.readlines())

for file, fname in zip(files, args.fnames):
    for linenum, line in enumerate(file, start=1):
        if toggle(args.searchfor, line, args.invert_match):
            print_line(line, fname, linenum)
