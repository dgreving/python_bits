import re
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument(
    'filename',
    )

args = parser.parse_args()

filename = args.filename
if filename == '-':
    input_method = sys.stdin
    text = input_method.read()
else:
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

replace_map = {
    '“': '"',
    '”': '"',
    '’': "'",
    '‘': "'",
    '–': '-',
    '—': '--',
    '…': '...',
    r'[ ]*\n': r'\n',
}

for original, replacement in replace_map.items():
    text = re.sub(original, replacement, text)

print(text, end='')
