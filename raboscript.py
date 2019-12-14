#!/usr/bin/env python3
import random
import argparse
from typing import Sequence, Iterator, List


END_PUNCT = '.!?…'


def skip_punct(words: Sequence[str], start_index: int) -> int:
    index = start_index
    while index < len(words):
        if words[index].isalnum():
            return index
        index += 1
    return index


def to_sentences(words: Sequence[str]) -> Iterator[Sequence[str]]:
    i = 0
    while i < len(words):
        sent = []
        i = skip_punct(words, i)
        while i < len(words) and words[i] not in END_PUNCT:
            sent.append(words[i])
            i += 1
        yield sent


def sent_effective_len(sent: Sequence[str]) -> int:
    return sum((1 for word in sent if word.isalnum()))


def raboficate(sents: Sequence[List[str]]) -> Sequence[str]:
    RABOWORDS = (
        ('много', '.'),
        ('малость', '.'),
        ('зачем', '?')
    )

    sents_rab = []
    for sent in sents:
        raboword = random.choice(RABOWORDS)
        sents_rab.append([raboword[0]] + sent + [raboword[1]])
    return sents_rab


def sents_to_text(sents: Sequence[Sequence[str]], lines_in_verse: int) -> str:
    SPACE = ' '
    NEWLINE = '\n'
    words = []
    line_num = 0
    for sent in sents:
        for i in range(len(sent)):
            if i == 0:
                words.append(sent[i].capitalize())
            elif sent[i] == ',':
                words.append(sent[i])
            elif i == len(sent) - 1:
                words.append(sent[i])
            else:
                words.append(SPACE + sent[i])
        words.append(NEWLINE)
        line_num += 1
        if line_num >= lines_in_verse:
            words.append(NEWLINE)
            line_num = 0
    return ''.join(words)


def main():
    parser = argparse.ArgumentParser(description='Рабоскрипт для генерации зомбирующей психозы.')
    parser.add_argument('--input_file', type=str, default='./data/glaza4.txt', help='Файл со входной психозой')
    parser.add_argument('--output_file', type=str, default='output.txt', help='Файл с выходной психозой')
    parser.add_argument('--min_sent_len', type=int, default=4, help='Минимальная эффективная длина рабофицируемого предложения')
    parser.add_argument('--max_sent_len', type=int, default=10, help='Максимальная эффективная длина рабофицируемого предложения')
    parser.add_argument('--result_sents', type=int, default=60, help='Количество выходных рабофицированных предложений')
    parser.add_argument('--lines_per_verse', type=int, default=6, help='Количество предложений в одном куплете')
    parser.add_argument('--pool_size', type=int, default=200, help='Количество предложений для рабофикации, случайно выбираемых из входной психозы')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    words = text.split(' ')
    sents = list(filter(lambda sent: sent_effective_len(sent) in range(args.min_sent_len, args.max_sent_len + 1), to_sentences(words)))

    sents_pool = []
    for _ in range(args.pool_size):
        sents_pool.append(random.choice(sents))
    sents_to_raboficate = []
    for _ in range(args.result_sents):
        sents_to_raboficate.append(random.choice(sents_pool))

    sents_rab = raboficate(sents_to_raboficate)
    rab = sents_to_text(sents_rab, args.lines_per_verse)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(rab)


if __name__ == '__main__':
    main()
