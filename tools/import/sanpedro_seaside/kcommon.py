# -*- coding: utf-8 -*-
"""Shared helpers for the San Pedro Seaside Villas translation files (same conventions as tools/import/k_almendro.py).
Tokens: {N107.82} decimal number, {G5000} grouped integer, {U} area unit."""
import json, re, sys
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
SP = '/Users/sasanraftari/Downloads/Sotomar_work'
TODO = json.load(open(f'{SP}/todo.json'))
ALL_PATHS = {p: en for en, paths in TODO.items() for p in paths}
T = {}


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def grouped(n, l):
    return f'{int(n):,}'.replace(',', GROUP[l])


def money(n, l):
    body = f'{int(n):,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(m.group(1), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{G(\d+)\}', lambda m: grouped(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def P(path, *tr):
    assert len(tr) == 9, (path, len(tr))
    assert path in ALL_PATHS, path
    en = ALL_PATHS[path]
    assert en not in T, ('duplicate', path)
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(path):
    en = ALL_PATHS[path]
    T[en] = {l: en for l in LOCS}


def finish(out, prefix=None):
    json.dump(T, open(f'{SP}/{out}', 'w'), ensure_ascii=False, indent=1)
    print('wrote', len(T), 'entries to', out)
