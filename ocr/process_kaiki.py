#!/usr/bin/python
import json
import re

# seed with a few words that we don't pick out properly
words = set(['meōpte', 'necesse', 'parum', 'quippe', 'suōpte', 'tuōpte'])
rare_words = set()

good_word = re.compile(r'^[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+$')

def clean_vowels(word):
    word = word.strip()
    word = word.replace('ă', 'a').replace('ĕ', 'e').replace('ĭ', 'i').replace('ŏ', 'o').replace('ŭ', 'u')
    word = word.replace('æ', 'ae')
    longword = word.replace('ā̆', 'ā').replace('ē̆', 'ē').replace('ī̆', 'ī').replace('ō̆', 'ō').replace('ū̆', 'ū')
    if good_word.match(longword) is None:
        return []
    shortword = word.replace('ā̆', 'a').replace('ē̆', 'e').replace('ī̆', 'i').replace('ō̆', 'o').replace('ū̆', 'u')
    if longword != shortword:
        return [longword, shortword]
    else:
        return [longword]

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
            clean_words = clean_vowels(form['form'].lstrip('*'))
            words.update(clean_words)
            if form['form'].startswith('*'):
                rare_words.update(clean_words)
    elif jline['pos'] in {'adv', 'conj', 'det', 'intj', 'prep'} and 'head_templates' in jline:
        for i in jline['head_templates']:
            words.update(clean_vowels(i['expansion'].split()[0]))
    elif jline['pos'] == 'num':
        # most (all?) numbers aren't macronized so this is okay
        words.update(clean_vowels(jline['word']))

words = sorted(words)

# output a full word list
with open('./latin_words_full.txt', 'w') as f:
    for w in words:
        f.write(w + '\n')

# output spelling dictionaries to use with vim, hunspell, etc
with open('./latin_words.dic', 'w') as f:
    f.write(f'{len(words)}\n')
    for w in words:
        if w in rare_words:
            f.write(w + '/?\n')
        else:
            f.write(w + '/QVN\n')

with open('./latin_words.aff', 'w') as f:
    f.write("""SET UTF-8

RARE ?

SFX Q Y 1
SFX Q 0 que .

SFX V Y 1
SFX V 0 ve .

SFX N Y 1
SFX N 0 ne .
""")
