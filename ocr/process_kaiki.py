#!/usr/bin/python
import json
import re

# seed with a few words that we don't pick out properly
raw_words = set(['necesse', 'parum'])

# get "all word forms" export json from https://kaikki.org/dictionary/Latin/index.html
for line in open('./kaikki.org-dictionary-Latin.json'):
    jline = json.loads(line)
    if 'forms' in jline:
        for form in jline['forms']:
            if 'inflection_template' in form.get('tags', set()):
                continue
            if 'table_tags' in form.get('tags', set()):
                continue
            if form['form'].startswith('-') or form['form'].startswith('/'):
                continue
            raw_words.add(form['form'].lstrip('*').strip())
    elif jline['pos'] in {'adv', 'conj', 'det', 'intj', 'prep'} and 'head_templates' in jline:
        for i in jline['head_templates']:
            raw_words.add(i['expansion'].split()[0])
    elif jline['pos'] == 'num':
        # most (all?) numbers aren't macronized so this is okay
        raw_words.add(jline['word'])

raw_words.remove('')

good_word = re.compile(r'^[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+$')

words = []
for word in raw_words:
    word = word.replace('ă', 'a').replace('ĕ', 'e').replace('ĭ', 'i').replace('ŏ', 'o').replace('ŭ', 'u')
    word = word.replace('æ', 'ae')
    longword = word.replace('ā̆', 'ā').replace('ē̆', 'ē').replace('ī̆', 'ī').replace('ō̆', 'ō').replace('ū̆', 'ū')
    if good_word.match(longword) is not None:
        words.append(longword)
        shortword = word.replace('ā̆', 'a').replace('ē̆', 'e').replace('ī̆', 'i').replace('ō̆', 'o').replace('ū̆', 'u')
        if longword != shortword:
            words.append(shortword)

words.sort()
with open('./latin_words.txt', 'w') as f:
    for w in words:
        f.write(w + '\n')
