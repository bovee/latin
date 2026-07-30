#!/usr/bin/python
import json
import re

# seed with a few words that we don't pick out properly
words = set()
rare_words = set()

good_word = re.compile(r'^[a-zA-ZæÆāēīōūȳǣĀĒĪŌŪȲǢġĠċĊþÞ]+$')
dirty_words = set()

def clean(word):
    word = word.strip()
    word = word.replace('Ð', 'Þ').replace('ð', 'þ')
    if good_word.match(word) is None:
        dirty_words.add(word)
        return []
    return [word]

# get "all word forms" export json from https://kaikki.org/
for line in open('./kaikki.org-dictionary-OldEnglish.jsonl'):
    jline = json.loads(line)
    if jline['pos'] in {'adv', 'conj', 'det', 'intj', 'prep'} and 'head_templates' in jline:
        for i in jline['head_templates']:
            clean_word = clean(i['expansion'])
            if ' ' in clean_word:
                continue
            words.update(clean_word)
    if 'forms' in jline:
        for form in jline['forms']:
            if 'inflection_template' in form.get('tags', set()):
                continue
            if 'table_tags' in form.get('tags', set()):
                continue
            clean_word = form['form'].lstrip('*')
            if clean_word.startswith('-') or clean_word.startswith('/') or clean_word.startswith('"'):
                continue
            if ' ' in clean_word:
                continue
            words.update(clean(clean_word))
            if form['form'].startswith('*'):
                rare_words.update([clean_word])

words = sorted(words)
assert 'ġīese' in words
assert 'eft' in words

# output a full word list
with open('./ang_words_full.txt', 'w') as f:
    for w in words:
        f.write(w + '\n')
