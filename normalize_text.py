#!/usr/bin/env python3
import re
import argparse
from typing import Sequence, Callable


PUNCTUATION = ',.!?…"«»—():/'
PUNCTUATION_RE = re.compile(f'([{re.escape(PUNCTUATION)}])')
ALLOWED_CHARS = set(PUNCTUATION + '-')
DASH = '—'


def normalize_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text)


def normalize_ellipsis(text: str) -> str:
    text = re.sub(r'(^|[^.])\.{2}([^.]|$)', r'\1.\2', text)
    return re.sub(r'(^|[^.])\.{3,}([^.]|$)', r'\1…\2', text)


def normalize_dashes(text: str) -> str:
    normalized_dash = ' ' + DASH + ' '
    return text.replace('—', normalized_dash) \
               .replace('–', normalized_dash) \
               .replace('--', normalized_dash) \
               .replace(' - ', normalized_dash) \
               .replace(' -', normalized_dash) \
               .replace('- ', normalized_dash)


def normalize_punctuation(text: str) -> str:
    return PUNCTUATION_RE.sub(r' \1 ', text)


def filter_text(text: str, allowed_functor: Callable[[str], bool]) -> str:
    return ''.join((c for c in text if allowed_functor(c)))


def main():
    parser = argparse.ArgumentParser(description='Скрипт для нормализации текста.')
    parser.add_argument('--input_file', type=str, default='input.txt', help='Файл со входной психозой')
    parser.add_argument('--output_file', type=str, default='output.txt', help='Файл с выходной психозой')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.lower()
    text = normalize_spaces(text)
    text = normalize_ellipsis(text)
    text = normalize_dashes(text)
    text = normalize_punctuation(text)
    text = filter_text(text, lambda c: c.isalnum() or c.isspace() or c in ALLOWED_CHARS)
    text = normalize_spaces(text)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    main()
