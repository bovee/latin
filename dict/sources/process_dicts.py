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
        stem1 = stem
        if '|' in stem:
            stem1 = stem.split('|')[0].strip()
        gen = map_options(lambda p: get_split_genitive(stem1, p), parts[0])
        return ('nom.', [stem, gen])

    if stem[-1] == 'ō' and parts[0].endswith('re'):
        # "normal" verbs
        return ('ver.', rebuild_normal_verb(stem, parts))
    elif stem[-1] == 'r' and parts[0].endswith('ī'):
        # deponent verbs
        return ('ver.', rebuild_depon_verb(stem, parts))
    elif stem[-1] == 't' and parts[0].endswith('re'):
        # third-person only verbs
        perf = '—'
        if len(parts) > 1:
            perf = parts[1]
        return ('ver.', [stem, parts[0], perf, '—'])
    elif stem[-1] == 'ī' and parts[0].endswith('isse'):
        # no present stem
        supine = '—'
        if len(parts) > 1:
            supine = parts[1]
        return ('ver.', [stem, '—', parts[0], supine])
    elif stem[-3:] == 'sum' and parts[0].endswith('e') and parts[1].endswith('ī'):
        # special case for sum and derivatives
        inf = stem[:-3] + 'esse' if parts[0].startswith('-') else parts[0]
        perf = stem[:-3] + 'fuī' if parts[1].startswith('-') else parts[1]
        return ('ver.', [stem, inf, perf, '—'])
    elif stem[-1] == 'ō' and parts[0].endswith('lle'):
        # special case for volō and derivatives
        return ('ver.', [stem, parts[0], parts[1], '—'])
    elif stem[-3:] == 'fīō' and parts[0].endswith('ī'):
        # special case for fīō
        return ('ver.', [stem, parts[0], parts[1], '—'])
    elif stem.endswith('ō') and parts == ['—']:
        return ('ver.', [stem, '—', '—', '—'])

    if parts == ['-a', '-um']:
        # 1st/2nd decl. adj.
        if stem.endswith('us'):
            return ('adi.', [stem[:-2] + '|us', stem[:-2] + '|a', stem[:-2] + '|um'])
        elif stem.endswith('r'):
            return ('adi.', [stem + '|', stem + '|a', stem + '|um'])
        else:
            raise Exception('Unknown 1st/2nd decl. adi.')
    elif len(parts) == 2 and parts[0].endswith('a') and parts[1].endswith('um'):
        # 1st/2nd decl. adj. with complex stem
        assert stem.endswith('r')
        assert join_ending(stem, parts[0]) is not None
        assert join_ending(stem, parts[1]) is not None
        f = join_ending(stem, parts[0])
        n = join_ending(stem, parts[1])
        return ('adi.', [stem + '|', f[:-1] + '|a', n[:-2] + '|um'])
    elif parts == ['-ae', '-a']:
        # 1st/2nd decl. adj., pl. only
        assert stem.endswith('ī')
        return ('adi.', [stem[:-1] + '|ī', stem[:-1] + '|ae', stem[:-1] + '|a'])
    elif len(parts) == 1 and parts[0].endswith('is'):
        # 3rd decl. adj., one termination
        if not parts[0].startswith('-'):
            return ('adi.', [stem, parts[0][:-2] + '|is', '—'])
        e = join_ending(stem, parts[0])
        if e is not None:
            # if consonant joining worked, return that
            return ('adi.', [stem, e[:-2] + '|is', '—'])
        if parts[0] == '-is':
            return ('adi.', [stem, stem + '|is', '—'])
        elif stem.endswith('x') and parts[0] == '-cis':
            return ('adi.', [stem, stem[:-1] + 'c|is', '—'])

        if parts[0][1] in VOWELS:
            for trunc_loc in range(-1, -len(stem), -1):
                trunc = stem[:trunc_loc]
                if trunc[-1] in VOWELS:
                    gen = trunc[:-1] + parts[0][1:]
                    return ('adi.', [stem, gen[:-2] + '|is', '—'])
        raise Exception('Unhandled third declension, one stem adi.')
    elif parts == ['-e']:
        # 3rd decl. adj., two terminations w/ i stem
        assert stem.endswith('is')
        return ('adi.', [stem[:-2] + '|is', stem[:-2] + '|is', stem[:-2] + '|e'])
    elif parts == ['-ae']:
        # 1st decl., one termination; just rūricola
        assert stem.endswith('a')
        return ('adi.', [stem, stem[:-2] + '|ae', '—'])
    elif len(parts) == 1 and parts[0].endswith('ius'):
        # 3rd decl. adj., two terminations w/ consonant stem
        assert stem.endswith('ior')
        return ('adi.', [stem[:-2] + '|or', stem[:-2] + '|or', stem[:-2] + '|us'])
    elif len(parts) == 2 and parts[0].endswith('is') and parts[1].endswith('e'):
        # 3rd decl. adj., three terminations
        assert stem.endswith('r')
        assert join_ending(stem, parts[0]) is not None
        assert join_ending(stem, parts[1]) is not None
        f = join_ending(stem, parts[0])
        n = join_ending(stem, parts[1])
        return ('adi.', [stem + '|', f[:-2] + '|is', n[:-1] + '|e'])

    if stem == 'quantuluscunque':
        return ('adi.', ['quantul|us|cunque', 'quantul|a|cunque', 'quantul|um|cunque'])

    raise Exception('Unhandled word')


VOWELS = {'a', 'e', 'i', 'o', 'u', 'ā', 'ē', 'ī', 'ō', 'ū'}

DECL_PATS = [
    ['a', '-ae'], # first decl
    ['ās', '-ae'], # first decl Greek
    ['ēs', '-ae'], # first decl Greek
    ['ē', '-ēs'], # first decl Greek
    ['ae', '-ārum'], # first decl plural
    ['us', '-ī'], # second decl m.
    ['os', '-ī'], # second decl m. (unknown variant?)
    ['um', '-ī'], # second decl n.
    ['ius', '-iī'], # second decl m. i-ending
    ['ium', '-iī'], # second decl n. i-ending
    ['ī', '-ōrum'], # second decl. plural
    ['a', '-ōrum'], # second decl. plural
    # second declension r's
    ['er', '-erī'],
    ['er', '-rī'],
    ['ber', '-berī'],
    ['ber', '-brī'],
    ['der', '-drī'],
    ['ter', '-trī'],
    # third declension other
    ['is', '-is'],
    ['ēs', '-is'],
    ['ō', '-inis'],
    ['ō', '-ōnis'],
    ['s', '-dis'],
    ['s', '-tis'],
    # third declension plural
    ['a', '-um'],
    ['ia', '-ium'],
    ['ēs', '-ium'],
    ['ēs', '-um'],
    # third declension Greek
    ['eus', '-eōs'],
    ['ōs', '-ōis'],
    ['ū', '-ūs'], # fourth declension
    ['us', '-ūs'], # fourth declension
    ['ō', '-ūs'], # fourth declension Greek
    ['ēs', '-eī'], # fifth declension
    ['ēs', '-ēī'], # fifth declension
]

SPECIAL_FORMS = {
    'rēspūblica':  're|ī|pūblic|ae',
    'iūsiūrandum': 'iūr|is|iūrand|ī',
    'Īdūs': 'Īd|uum',
}

def demacro(word):
    return word.replace('ā', 'i').replace('ē', 'i').replace('ī', 'i').replace('ō', 'i').replace('ū', 'i').replace('a', 'i').replace('e', 'i').replace('o', 'i').replace('u', 'i').replace('x', 'c')


def join_ending(stem, ending):
    if not ending.startswith('-'):
        return ending

    if ending[1] not in VOWELS:
        for trunc_loc in range(-1, -len(stem), -1):
            trunc = stem[:trunc_loc]
            if trunc[-1] == ending[1]:
                return trunc + ending[2:]
    return None


def get_split_genitive(stem, ending):
    if stem in SPECIAL_FORMS:
        return SPECIAL_FORMS[stem]
    for stem_ending, gen_form in DECL_PATS:
        if stem.endswith(stem_ending) and ending == gen_form:
            if gen_form.endswith('is'):
                return stem[:-len(stem_ending)] + gen_form[1:-2] + '|is'
            elif gen_form.endswith('ī') and gen_form[-2] not in {'e', 'ē', 'i'}:
                return stem[:-len(stem_ending)] + gen_form[1:-1] + '|ī'
            else:
                return stem[:-len(stem_ending)] + '|' + gen_form[1:]

    if ending.startswith('-') and ending.endswith('is'):
        old = demacro(stem[-len(ending) + 3:])
        new = demacro(ending[1:-2])

        if len(new) > 1 and old[:-1] == new[:-1]:
            return stem[:-len(new)] + ending[1:-2] + '|is'
        if old == new:
            return stem[:-len(new)] + ending[1:-2] + '|is'

        if stem.endswith('ō') and ending == '-nis':
            return stem + 'n|is'
        elif stem.endswith('er') and ending.endswith('ris'):
            return stem[:-len(new) - 1] + ending[1:-2] + '|is'

    if stem.endswith('r') and ending == '-ī':
        # second declension '-r' is not removed
        return stem + '|ī'
    if ending.endswith('ae'):
        return ending[:-2] + '|ae'
    elif stem.endswith('us') and ending.endswith('ī'):
        # second declension
        return ending[:-1] + '|ī'
    elif stem.endswith('er') and ending.endswith('rī'):
        # second declension (r shift)
        return ending[:-1] + '|ī'
    elif ending.endswith('is'):
        # third declension, parisyllabic i-stem
        return ending[:-2] + '|is'
    elif stem.endswith('ēs') and (ending.endswith('eī') or ending.endswith('ēī')):
        # fifth declension
        return ending[:-2] + '|' + ending[-2:]

    if not ending.startswith('-') and ending.endswith('os'):
        return ending[:-2] + '|os'

    raise Exception('Genitive of noun could not be determined')

def rebuild_normal_verb(stem, parts):
    if parts[0].endswith('ferre'):
        assert stem.endswith('ferō')
        return [stem] + [p if not p.startswith('-') else stem[:-4] + p[1:] for p in parts]
    if parts[0] == '-dare':
        assert stem.endswith('dō')
        # irregular; not a long a
        return [stem] + [p if not p.startswith('-') else stem[:-2] + p[1:] for p in parts]

    assert parts[0][-3:] in {'āre', 'ere', 'ēre', 'īre'}
    if parts[0] not in {'-āre', '-ere', '-ēre', '-īre'}:
        return [stem] + parts
    if len(parts) == 1:
        inf = get_infinitive(stem, parts[0])
        if inf.endswith('āre'):
            perf = get_perfect(inf, '-āvī')
            partic = get_supine(inf, '-ātum')
        elif inf.endswith('ēre'):
            perf = get_perfect(inf, '-uī')
            partic = get_supine(inf, '-itum')
        elif inf.endswith('ere'):
            # special case for 3rd conj verbs w/o perfect or supine forms
            assert stem in {'mītēscō', 'glīscō'}
            perf = '—'
            partic = '—'
        elif inf.endswith('īre'):
            perf = get_perfect(inf, '-īvī')
            partic = get_supine(inf, '-ītum')

        return [stem, inf, perf, partic]
    elif len(parts) == 2:
        inf = get_infinitive(stem, parts[0])
        assert inf is not None
        if parts[1].endswith('um'):
            # no perfect, but there is a supine
            partic = map_options(lambda p: get_supine(inf, p), parts[1])
            return [stem, inf, '—', partic]
        # no supine, but there is a perfect
        assert parts[1].endswith('ī')
        perf = map_options(lambda p: get_perfect(inf, p), parts[1])
        return [stem, inf, perf, '—']
    elif len(parts) == 3:
        inf = get_infinitive(stem, parts[0])
        assert inf is not None
        perf = map_options(lambda p: get_perfect(inf, p), parts[1])
        partic = map_options(lambda p: get_supine(inf, p), parts[2])
        return [stem, inf, perf, partic]
    raise Exception('Verb parts unknown')


def rebuild_depon_verb(stem, parts):
    inf = None
    if not parts[0].startswith('-'):
        inf = parts[0]
    if stem.endswith('ior') and parts[0] in ('-ī', '-īrī'):
        inf = stem[:-3] + parts[0][1:]
    elif stem.endswith('eor') and parts[0] == '-ērī':
        inf = stem[:-3] + parts[0][1:]
    elif stem.endswith('or') and parts[0] in ('-ārī', '-ī'):
        inf = stem[:-2] + parts[0][1:]
    assert inf is not None

    perf = '—'
    if len(parts) > 1:
        part1 = parts[1][:-4] if parts[1].endswith(' sum') else parts[1]
        if not part1.startswith('-'):
            perf = part1
        elif part1 == '-ātus':
            perf = stem[:-2] + part1[1:]
        elif stem.endswith('ior') and part1 == '-ītus':
            perf = stem[:-3] + part1[1:]
        else:
            perf = join_ending(stem[:-2], part1)
        assert perf != '—'

    return [stem, inf, perf, '—']


def map_options(function, ending):
    if '|' in ending:
        return ' | '.join(map(function, ending.split(' | ')))
    else:
        return function(ending)

def get_infinitive(stem, ending):
    if not ending.startswith('-'):
        return ending
    elif ending == '-āre':
        return stem[:-1] + ending[1:]
    elif ending == '-ēre' and stem.endswith('eō'):
        return stem[:-2] + ending[1:]
    elif ending == '-ere' and stem.endswith('iō'):
        return stem[:-2] + ending[1:]
    elif ending == '-ere':
        return stem[:-1] + ending[1:]
    elif ending == '-īre' and stem.endswith('iō'):
        return stem[:-2] + ending[1:]
    elif ending == '-īre' and stem.endswith('eō'):
        # derivatives of "eo"
        return stem[:-2] + ending[1:]
    raise Exception('Infinitive could not be formed')


def get_perfect(inf, ending):
    if '|' in ending:
        raise Exception('Unexpected | in perfect; please split outside')
    if not ending.startswith('-'):
        # TODO: maybe check endings aren't too short (e.g. just missing a dash)?
        return ending
    elif inf.endswith('āre') and ending in ('-āvī', '-uī'):
        return inf[:-3] + ending[1:]
    elif inf.endswith('ēre') and ending == '-uī':
        return inf[:-3] + ending[1:]
    elif inf.endswith('dere') and ending in ('-dī', '-sī'):
        return inf[:-4] + ending[1:]
    elif inf.endswith('gere') and ending == '-sī':
        return inf[:-4] + ending[1:]
    elif inf.endswith('dēre') and ending == '-sī':
        return inf[:-4] + ending[1:]
    elif inf.endswith('icere') and ending == '-iēcī':
        return inf[:-5] + ending[1:]
    elif inf.endswith('uere') and ending == '-uī':
        return inf[:-4] + ending[1:]
    elif inf.endswith('ere') and ending in ('-īvī', '-iī', '-uī'):
        return inf[:-3] + ending[1:]
    elif inf.endswith('īre') and ending in ('-īvī', '-iī', '-uī'):
        return inf[:-3] + ending[1:]

    j = join_ending(inf[:-2], ending)
    assert j is not None
    return j


def get_supine(inf, ending):
    if '|' in ending:
        raise Exception('Unexpected | in supine; please split outside')
    if not ending.startswith('-'):
        return ending
    elif inf.endswith('āre') and ending in ('-ātum', '-itum'):
        return inf[:-3] + ending[1:]
    elif inf.endswith('ēre') and ending == '-itum':
        return inf[:-3] + ending[1:]
    elif inf.endswith('dere') and ending == '-sum':
        return inf[:-4] + ending[1:]
    elif inf.endswith('iere') and ending == '-ītum':
        return inf[:-4] + ending[1:]
    elif inf.endswith('tere') and ending == '-sum':
        return inf[:-4] + ending[1:]
    elif inf.endswith('uere') and ending == '-ūtum':
        return inf[:-4] + ending[1:]
    elif inf.endswith('ere') and ending == '-ītum':
        return inf[:-3] + ending[1:]
    elif inf.endswith('icere') and ending == '-iectum':
        return inf[:-5] + ending[1:]
    elif inf.endswith('īre') and ending in ('-itum', '-ītum'):
        return inf[:-3] + ending[1:]

    j = join_ending(inf[:-2], ending)
    assert j is not None
    return j


gender_re = re.compile(r"\((m?\.?f?\.??n?\.?)\)")

files = [
    (open('dict_strange_ovid.txt'), ':', False),
    (open('dict_paine_sec.txt'), '.', False),
    (open('dict_dale.txt'), ':', False),
    (open('dict_app_fab.txt'), ';', True),
    (open('dict_app_pons.txt'), ';', True),
]

words = dict()
word_types = Counter()
suffs = Counter()

for f, head_delim, parenthetical_gender in files:
    even = True
    print(f'###{f.name}')
    book_abbrev = {
     'dict_app_fab.txt': 'F',
     'dict_app_pons.txt': 'PT',
     'dict_dale.txt': 'RCR',
     'dict_paine_sec.txt': 'SA',
     'dict_strange_ovid.txt': 'ONE',
    }[f.name]
    for line in f:
        even = not even
        if even:
            if line.strip() != '':
                raise Exception('LINE SHOULD BE EMPTY:', line)
                break
            continue
        if head_delim not in line:
            raise Exception('NO DELIM:', line)
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
    
        labelled_word_type = None
        if not parenthetical_gender:
            if len(parts) > 0 and parts[-1] in {'f.', 'm.', 'n.', 'c.', 'm.f.', 'm. et f.'}:
                gender = parts.pop()
                if gender == 'm. et f.':
                    gender = 'm.f.'
                elif gender == 'c.':
                    gender = 'm.f.'
            elif len(parts) > 0 and parts[-1] in {'f', 'm', 'n', 'c'}:
                gender = parts.pop() + '.'
                if gender == 'c.':
                    gender = 'm.f.'
            elif len(parts) > 0 and parts[-1].endswith('.'):
                labelled_word_type = parts.pop()
            elif len(parts) > 0 and parts[-1] in {'adiect', 'adv', 'coniūnct', 'excl'}:
                labelled_word_type = parts.pop() + '.'

        word_type, entry = guess_type(stem, parts, gender)
        if word_type == 'indecl.':
            word_type = {
                'coni.': 'con.',
                'coniūnct.': 'con.',
                'adv.': 'adv.',
                'excl.': 'int.',
            }.get(labelled_word_type, 'ind.')
            if '...' in stem:
                word_type = 'gra.'

        if len(defn.strip()):
            defn = f'[{book_abbrev}] {defn.strip().replace(';','.')}'
        else:
            defn = ''
        
        entry = {
            'gender': gender,
            'type': word_type,
            'entry': entry,
            'defn': defn,
        }
        if stem in words:
            words[stem].append(entry)
        else:
            words[stem] = [entry]
        word_types.update([word_type])

f.close()

verbs = {}
adjec = {}
nouns = {}
indec = {}
for w in words:
    entries = words[w]
    for e in entries:
        if e['type'] == 'ver.':
            if w not in verbs:
                verbs[w] = [e]
            else:
                for v in verbs[w]:
                    align2 = None
                    align3 = None
                    align4 = None
                    if v['entry'][1] == e['entry'][1]:
                        align2 = v['entry'][1]

                    if v['entry'][2] == e['entry'][2]:
                        align3 = v['entry'][2]
                    elif v['entry'][2] in e['entry'][2].split(' | '):
                        align3 = e['entry'][2]
                    elif e['entry'][2] in v['entry'][2].split(' | '):
                        align3 = v['entry'][2]
                    elif e['entry'][2] == '—':
                        align3 = v['entry'][2]
                    elif v['entry'][2] == '—':
                        align3 = e['entry'][2]
                    elif e['entry'][2][:-3] == v['entry'][2][:-2] and e['entry'][2].endswith('īvī') and v['entry'][2].endswith('iī'):
                        align3 = e['entry'][2] + ' | ' + v['entry'][2]
                    elif e['entry'][2][:-2] == v['entry'][2][:-3] and e['entry'][2].endswith('iī') and v['entry'][2].endswith('īvī'):
                        align3 = e['entry'][2] + ' | ' + v['entry'][2]

                    if v['entry'][3] == e['entry'][3]:
                        align4 = v['entry'][3]
                    elif v['entry'][3] in e['entry'][3].split(' | '):
                        align4 = e['entry'][3]
                    elif e['entry'][3] in v['entry'][3].split(' | '):
                        align4 = v['entry'][3]
                    elif e['entry'][3] == '—':
                        align4 = v['entry'][3]
                    elif v['entry'][3] == '—':
                        align4 = e['entry'][3]

                    if align2 is not None and align3 is not None and align4 is not None:
                        v['entry'][1] = align2
                        v['entry'][2] = align3
                        v['entry'][3] = align4
                        v['defn'] += ' ' + e['defn']
                        break
                else:
                    verbs[w] += [e]
        elif e['type'] == 'adi.':
            if w not in adjec:
                adjec[w] = [e]
            else:
                for a in adjec[w]:
                    if a['entry'] == e['entry']:
                        a['defn'] += ' ' + e['defn']
                        break
                else:
                    adjec[w] += [e]
        elif e['type'] == 'nom.':
            if w not in nouns:
                nouns[w] = [e]
            else:
                for n in nouns[w]:
                    if n['entry'] == e['entry']:
                        if n['gender'] != e['gender']:
                            n[w] = 'm.f.'
                        n['defn'] += ' ' + e['defn']
                        break
                else:
                    nouns[w] += [e]
        else:
            if w not in indec:
                indec[w] = [e]
            else:
                indec[w][0]['defn'] += ' ' + e['defn']

for v in verbs:
    if v in indec:
        indec[v].extend(verbs[v])
    else:
        indec[v] = verbs[v]
for a in adjec:
    if a in indec:
        indec[a].extend(adjec[a])
    else:
        indec[a] = adjec[a]
for n in nouns:
    if n in indec:
        indec[n].extend(nouns[n])
    else:
        indec[n] = nouns[n]

with open('dict.txt', 'w') as f:
    for i in sorted(indec, key=lambda w: w.lower().replace('ā', 'a').replace('ē', 'e').replace('ī', 'i').replace('ō', 'o').replace('ū', 'u')):
        for w in indec[i]:
            word_type = (w['type'] if w['gender'] is None else w['gender']).replace('.', '')
            f.write(f'{','.join(w['entry'])};{word_type};{w['defn']}\n')
