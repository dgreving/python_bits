import csv
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    'from_fname')

parser.add_argument(
    'to_fname')

parser.add_argument(
    '--in-delimiter',
    default=None,
    dest='indel'
    )

parser.add_argument(
    '--in-quote',
    default='"',
    dest='inquote'
    )

args = parser.parse_args()


with open(args.from_fname, 'r') as f:
    if not args.indel:
        reader = csv.reader(f, dialect=csv.Sniffer().sniff(f.read(1024)))
        f.seek(0)
    else:
        reader = csv.reader(f, delimiter=args.indel, quotechar=args.inquote)
    with open(args.to_fname, 'w') as f2:
        writer = csv.writer(
            f2,
            dialect='unix',
            delimiter=',',
            quoting=csv.QUOTE_MINIMAL,
            )
        for row in reader:
            writer.writerow(row)
