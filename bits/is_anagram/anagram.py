from unicodedata import normalize


def clean_spaces(word):
    return word.replace(' ', '')


def clean_accents(word):
    return ''.join([normalize('NFD', x)[0] for x in word])


def clean_punctuation(word):
    return ''.join([x for x in word if x.isalpha()])


def is_anagram(word1, word2):
    for func in (clean_spaces, clean_accents, clean_punctuation):
        word1, word2 = func(word1), func(word2)
    if len(word1) != len(word2):
        return False
    letters1, letters2 = sorted(word1.lower()), sorted(word2.lower())
    return all(a == b for a, b in zip(letters1, letters2))
