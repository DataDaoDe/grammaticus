from typing import Optional, List, Any
from grammaticus.utils import data_filepath
from grammaticus.languages.latin.nouns.common import Noun
import pandas as pd
import numpy as np

EXCEPTION_WORDS = pd.read_csv(data_filepath(
    'nouns/first_declension/exceptions.csv'), sep="|")

CASE_ENDINGS = pd.DataFrame({
    'nominative': ['a', 'ae'],
    'genitive': ['ae', 'arum'],
    'dative': ['ae', 'is'],
    'accusative': ['am', 'as'],
    'ablative': ['a', 'is'],
    'vocative': ['a', 'ae'],
}, index=['singular', 'plural'])
SORTED_CASE_ENDINGS = sorted(CASE_ENDINGS.to_numpy().ravel(),
                             key=len, reverse=True)


class FirstDeclensionNoun(Noun):
    def __init__(self, stem: str):
        self._exception = False
        if stem in EXCEPTION_WORDS['stem'].values:
            self._exception = True
            self._exception_item = EXCEPTION_WORDS[EXCEPTION_WORDS['stem']
                                                   == stem].iloc[0]
            gender = self._exception_item['gender']
        else:
            gender = 'f'
        super().__init__(stem, gender, 'I', None)

    def decline(self, cmd: str) -> str:
        cmd = cmd.lower().strip()
        stem = self._stem
        if self._exception and self._exception_item['irregular_endings']:
            return 'has irregular endings'
        else:
            if cmd == 'noms' or cmd == 'vocs':
                return '{}{}'.format(stem, CASE_ENDINGS['nominative']['singular'])
            elif cmd == 'nomp' or cmd == 'vop':
                return '{}{}'.format(stem, CASE_ENDINGS['nominative']['plural'])
            elif cmd == 'accs':
                return '{}{}'.format(stem, CASE_ENDINGS['accusative']['singular'])
            elif cmd == 'accp':
                return '{}{}'.format(stem, CASE_ENDINGS['accusative']['plural'])
            elif cmd == 'gens':
                return '{}{}'.format(stem, CASE_ENDINGS['genitive']['singular'])
            elif cmd == 'genp':
                return '{}{}'.format(stem, CASE_ENDINGS['genitive']['plural'])
            elif cmd == 'dats':
                return '{}{}'.format(stem, CASE_ENDINGS['dative']['singular'])
            elif cmd == 'datp':
                return '{}{}'.format(stem, CASE_ENDINGS['dative']['plural'])
            elif cmd == 'abls':
                return '{}{}'.format(stem, CASE_ENDINGS['ablative']['singular'])
            elif cmd == 'ablp':
                return '{}{}'.format(stem, CASE_ENDINGS['ablative']['plural'])


def parse_word(word: str) -> Noun:
    # get the stem
    stem = get_stem(word)
    if not stem:
        raise ValueError(
            'unable to get the stem of: {}. Is it first declension?'.format(word))
    return Noun(stem=stem, gender='f', declension=1)


def get_stem(word: str) -> Optional[str]:
    # start with longest
    for end in SORTED_CASE_ENDINGS:
        if word.endswith(end):
            stem = word[:(word.rindex(end))]
            return stem


def is_first_declension_noun(word: str) -> bool:
    for end in SORTED_CASE_ENDINGS:
        if word.endswith(end):
            return True
    df = pd.read_csv(data_filepath(
        'nouns/first_declension/exceptions.csv'), sep='|')

    # we only need to look at the irregular words, the others have regular endings and thus
    # have already been checked with the above code.
    irr = df[df['irregular'] == True]
    for idx, row in irr.iterrows():
        irr_endings = [e.split(',') for e in row['endings'].split(':')]
        sorted_irr_endings = sorted(
            np.ravel(irr_endings), key=len, reverse=True)
        for end in sorted_irr_endings:
            if word.endswith(end) and word == '{}{}'.format(row['stem'], end):
                return True


def decline(stem: str, declension) -> pd.DataFrame:

    forms = declension.copy(deep=True)
    for case in CASES:
        forms[case] = forms[case].apply(
            lambda x: '{}{}'.format(stem, x))

    return forms
