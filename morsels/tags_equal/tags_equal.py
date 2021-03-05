import shlex


def parse_tag(t):
    tag_dict = {}
    elements = shlex.split(t[1:-1].lower())
    tag_dict['name'] = elements[0]
    for element in elements[1:]:
        key, _, val = element.partition('=')
        if key not in tag_dict:
            tag_dict[key] = val.strip('"\'')
    return tag_dict


def tags_equal(t1, t2):
    d1, d2 = parse_tag(t1), parse_tag(t2)
    return d1 == d2
