#!/usr/bin/python 

from collections import Counter
import re

stems = {}

def guess_type(stem, parts, gender=None):
    if len(parts) > 0 and parts[0] in {'1', '2', '3', '4'}:
        if stem[-1] == 'ō':
            parts[0] = {'1': '-āre', '2': '-ēre', '3': '-ere', '4': '-īre'}[parts[0]]
        elif stem[-1] == 'r':
            parts[0] = {'1': '-ārī', '2': '-ērī', '3': '-ī', '4': '-īrī'}[parts[0]]

    if stem in stems:
        stems[stem].add(tuple(parts))
    else:
        stems[stem] = set([tuple(parts)])

    if len(parts) == 0:
        return ('indecl.', [stem])
    if gender is not None:
        count_declensions(stem, parts)
        return ('nomin.', rebuild_noun(stem, parts))

    if stem[-1] == 'ō' and parts[0].endswith('re'):
        # "normal" verbs
        return ('verb.', rebuild_normal_verb(stem, parts))
    elif stem[-1] == 'r' and parts[0].endswith('ī'):
        # deponent verbs
        return ('verb.', [])
    elif stem[-1] == 't' and parts[0].endswith('re'):
        # third-person only verbs
        return ('verb.', [])
    elif stem[-1] == 'ī' and parts[0].endswith('isse'):
        # no present stem
        return ('verb.', [])
    elif stem[-3:] == 'sum' and len(parts) == 2 and parts[0].endswith('e') and parts[1].endswith('ī'):
        # special case for sum and derivatives
        return ('verb.', [])
    elif stem[-1] == 'ō' and parts[0].endswith('lle'):
        # special case for volō and derivatives
        return ('verb.', [])
    elif stem[-3:] == 'fīō' and parts[0].endswith('ī'):
        # special case for fīō
        return ('verb.', [])

    if parts == ['-a', '-um']:
        # 1st/2nd decl. adj.
        return ('adi.', [])
    elif len(parts) == 2 and parts[0].endswith('a') and parts[1].endswith('um'):
        # 1st/2nd decl. adj. with complex stem
        return ('adi.', [])
    elif parts == ['-ae', '-a']:
        # 1st/2nd decl. adj., pl. only
        return ('adi.', [])
    elif len(parts) == 1 and parts[0].endswith('is'):
        # 3rd decl. adj., one termination
        return ('adi.', [])
    elif parts == ['-e']:
        # 3rd decl. adj., two terminations w/ i stem
        return ('adi.', [])
    elif len(parts) == 1 and parts[0].endswith('us'):
        # 3rd decl. adj., two terminations w/ consonant stem
        return ('adi.', [])
    elif len(parts) == 2 and parts[0].endswith('is') and parts[1].endswith('e'):
        # 3rd decl. adj., three terminations
        return ('adi.', [])

    print(stem, parts)
    return ('', [])

noun_decls = Counter()
def count_declensions(stem, parts):
    ENDINGS = {'ae': '1', 'ēs': '1g', 'ārum': '1pl', 'rī': '2', 'iī': '2', 'ōrum': '2pl', 'is': '3', 'um': '3pl', 'ūs': '4', 'uum': '4pl', 'eī': '5', 'ēī': '5'}
    for ending, decl in ENDINGS.items():
        if parts[0].endswith(ending):
            noun_decls.update([decl])
            break
    else:
        if parts[0] == '-ī':
            noun_decls.update(['2'])
        else:
            noun_decls.update([parts[0]])


def rebuild_noun(stem, parts):
    return []

def rebuild_normal_verb(stem, parts):
    if parts[0].endswith('ferre'):
        return
    if parts[0] == '-dare':
        return  # irregular; not a long a
    assert parts[0][-3:] in {'āre', 'ere', 'ēre', 'īre'}
    # TODO: figure out how to add stem to -āre, -ere, etc
    return []


gender_re = re.compile(r"\((m?\.?f?\.??n?\.?)\)")

files = [
    (open('dict_strange_ovid.txt'), ':', False),
    (open('dict_paine_sec.txt'), '.', False),
    (open('dict_dale.txt'), ':', False),
    (open('dict_app_fab.txt'), ';', True),
    (open('dict_app_pons.txt'), ';', True),
]

word_types = Counter()
suffs = Counter()

for f, head_delim, parenthetical_gender in files:
    even = True
    print(f'###{f.name}')
    for line in f:
        even = not even
        if even:
            if line.strip() != '':
                print('LINE SHOULD BE EMPTY:', line)
                break
            continue
        if head_delim not in line:
            print('NO DELIM:', line)
            continue
        header, defn = line.strip().split(head_delim, maxsplit=1)
        gender = None
        if parenthetical_gender:
            gender = gender_re.search(header)
            if gender is not None:
                header = gender_re.sub('', header)
                gender = gender.groups()[0]
    
        stem, *parts = header.split(',')
        parts = [p.strip() for p in parts]
    
        if not parenthetical_gender:
            if len(parts) > 0 and parts[-1] in {'f.', 'm.', 'n.', 'm.f.', 'm. et f.'}:
                gender = parts.pop()
                if gender == 'm. et f.':
                    gender = 'm.f.'
            elif len(parts) > 0 and parts[-1] in {'f', 'm', 'n', 'c'}:
                gender = parts.pop() + '.'
                if gender == 'c.':
                    gender = 'm.f.'
            elif len(parts) > 0 and parts[-1].endswith('.'):
                labelled_word_type = parts.pop()
            elif len(parts) > 0 and parts[-1] in {'adiect', 'adv', 'coniūnct', 'excl'}:
                labelled_word_type = parts.pop() + '.'
            elif len(parts) > 0 and parts[-1] == '—':
                parts = parts[:-1]

        word_type, entry = guess_type(stem, parts, gender)
        word_types.update([word_type])

    last_line = line

print(word_types)

f.close()
