#!/usr/bin/env python3
import re
from typing import Sequence, Tuple, Callable

from normalize_text import *


def generic_test_normalization(table: Sequence[Tuple[str, str]], function: Callable[[str], str]):
    for (input_text, output_pattern) in table:
            assert re.match(output_pattern, function(input_text)) is not None


def test_normalize_spaces():
    table = (
        ('', r''),
        (' ', r' '),
        ('  ', r' '),
        ('\t\t', r' '),
        ('\t \t', r' '),
        (' xyz ', r' xyz '),
        (' \nxyz   \naaa\n', r' xyz aaa '),
        ('Hello  World!\nWhat\'s\t up?', r'Hello World! What\'s up\?')
    )
    generic_test_normalization(table, normalize_spaces)


def test_normalize_ellipsis():
    table = (
        ('', r''),
        ('...', r'…'),
        ('..', r'\.'),
        ('....', r'…'),
        ('....\n..', r'…\n.'),
        ('xyz........', r'xyz…'),
        ('...xyz', r'…xyz'),
        ('..xyz', r'\.xyz'),
        ('x... y...', r'x… y…')
    )
    generic_test_normalization(table, normalize_ellipsis)


def test_normalize_dashes():
    table = (
        ('', r''),
        (' xx – yy ', r' xx +— + yy '),
        ('-', r'\-'),
        ('xx-yy', r'xx\-yy'),  # hyphen
        ('xx–yy', r'xx +— +yy'),  # en-dash
        ('xx—yy', r'xx +— +yy'),  # em-dash
        ('xx -yy', r'xx +— +yy'),
        ('xx- yy', r'xx +— +yy'),
        ('xx - yy', r'xx +— +yy'),
        ('xx--yy', r'xx +— +yy'),
        (' —xx', r' +— +xx')
    )
    generic_test_normalization(table, normalize_dashes)


def test_normalize_punctuation():
    table = [
        ('', r''),
        ('x!', r'x ! '),
        ('?!?!?', r' +\? +! +\? +! +\? +')
    ]
    for c in PUNCTUATION:
        table.append((f'xx{c}', f'xx +{re.escape(c)} +'))
        table.append((f'{c}yy', f' +{re.escape(c)} +yy'))
        table.append((f'xx{c}yy', f'xx +{re.escape(c)} +yy'))

    generic_test_normalization(table, normalize_punctuation)


def test_filter_text():
    functors_table = (
        (lambda c: False, (
            ('', ''),
            ('xyz', '')
        )),
        (lambda c: True, (
            ('', ''),
            ('xyz', 'xyz')
        )),
        (lambda c: c == 'x' or c == 'y', (
            ('', ''),
            ('zzz', ''),
            ('z12 xyz', 'xy')
        ))
    )
    for functor, cases in functors_table:
        for input_text, output_text in cases:
            assert filter_text(input_text, functor) == output_text


def main():
    test_normalize_spaces()
    test_normalize_ellipsis()
    test_normalize_dashes()
    test_normalize_punctuation()
    test_filter_text()


if __name__ == '__main__':
    main()
