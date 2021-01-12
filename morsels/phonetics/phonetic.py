import argparse
from unicodedata import normalize


parser = argparse.ArgumentParser()

parser.add_argument(
    'phrase',
    help='phrase to convert',
    nargs='*',
    )

parser.add_argument(
    '-f', '--filename',
    help='filename',
    default=None,
    )

args = parser.parse_args()

codes = {
    'a': "Alfa",
    'b': "Bravo",
    'c': "Charlie",
    'd': "Delta",
    'e': "Echo",
    'f': "Foxtrot",
    'g': "Golf",
    'h': "Hotel",
    'i': "India",
    'j': "Juliett",
    'k': "Kilo",
    'l': "Lima",
    'm': "Mike",
    'n': "November",
    'o': "Oscar",
    'p': "Papa",
    'q': "Quebec",
    'r': "Romeo",
    's': "Sierra",
    't': "Tango",
    'u': "Uniform",
    'v': "Victor",
    'w': "Whiskey",
    'x': "XRay",
    'y': "Yankee",
    'z': "Zulu",
    '0': "Zero",
    '1': "One",
    '2': "Two",
    '3': "Three",
    '4': "Four",
    '5': "Five",
    '6': "Six",
    '7': "Seven",
    '8': "Eight",
    '9': "Nine",
    ' ': '',
}

if args.filename:
    with open(args.filename, 'r') as f:
        codes = {' ': ''}
        for line in f.readlines():
            key, val = line.strip('\n').split(' ')
            codes[key] = val

if not args.phrase:
    args.phrase = [input('Text to spell out: ')]

phrase = ' '.join(args.phrase)

converted = [
    codes[normalize('NFD', letter)[0].lower()]
    for letter in phrase
    if letter.isalnum() or letter == ' ']


for word in converted:
    print(word)
