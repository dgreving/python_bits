from collections import defaultdict
import re


def count_words(s):
    counts = defaultdict(int)
    words = s.lower().split()
    for word in words:
        word = re.sub("[^a-zA-Z0-9']+", "", word)
        counts[word] += 1
    return counts
