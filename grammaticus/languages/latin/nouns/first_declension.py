from typing import Optional, List, Any, Dict
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


def extract_ending(seq: str, index: int = None) -> str:
    if ':' in seq:
        parts = seq.split(':')
        if index:
            return parts[index]
        else:
            return parts[0]
    else:
        return seq


def _stem_ending_formatter(stem: str, s: pd.Series, idx: int = 0) -> str:
    v = s.split(',')
    ending = extract_ending(v[idx])
    return '{}{}'.format(stem, ending)


class FirstDeclensionNoun(Noun):

    def __init__(self, stem: str):
        self._exception = False
        if (stem in EXCEPTION_WORDS['stem'].values) or (stem in EXCEPTION_WORDS['alt_stems'].values):
            self._exception = True
            if stem in EXCEPTION_WORDS['stem'].values:
                self._exception_item = EXCEPTION_WORDS.loc[EXCEPTION_WORDS['stem']
                                                           == stem].iloc[0]
            elif stem in EXCEPTION_WORDS['alt_stems']:
                self._exception_item = EXCEPTION_WORDS.loc[EXCEPTION_WORDS['alt_stems'].str.contains(
                    stem).fillna(False)].iloc[0]
            gender = self._exception_item['gender']
        else:
            gender = 'f'
        super().__init__(stem, gender, 'I', None)

    def get_case_info(self, form: str) -> Dict[Any, Any]:
        ending = form[len(self._stem):]
        g = {'cases': []}
        if self._exception and self._exception_item['irregular']:
            item = self._exception_item
            endings = [
                {'k': 'nom', 'v': item['nom'].split(',')},
                {'k': 'gen', 'v': item['gen'].split(',')},
                {'k': 'acc', 'v': item['acc'].split(',')},
                {'k': 'dat', 'v': item['dat'].split(',')},
                {'k': 'abl', 'v': item['abl'].split(',')},
                {'k': 'voc', 'v': item['voc'].split(',')},
            ]
            for idx in range(0, len(endings)):
                h = endings[idx]
                case_name = h['k']
                case_values = list(map(lambda x: x.split(":"), h['v']))

                # singular values
                i = '{}s'.format(case_name)
                for v in case_values[0]:
                    if ending == v:
                        if i not in g['cases']:
                            g['cases'].append(i)
                # plural values
                p = '{}p'.format(case_name)
                for v in case_values[1]:
                    if ending == v:
                        if i not in g['cases']:
                            g['cases'].append(p)
        else:
            for idx, row in CASE_ENDINGS.iterrows():
                sop = 's' if idx == 'singular' else 'p'
                if row['nominative'] == ending:
                    g['cases'].append('nom{}'.format(sop))
                if row['accusative'] == ending:
                    g['cases'].append('acc{}'.format(sop))
                if row['genitive'] == ending:
                    g['cases'].append('gen{}'.format(sop))
                if row['dative'] == ending:
                    g['cases'].append('dat{}'.format(sop))
                if row['ablative'] == ending:
                    g['cases'].append('abl{}'.format(sop))
                if row['vocative'] == ending:
                    g['cases'].append('voc{}'.format(sop))
        return g['cases']

    def decline(self, cmd: str) -> str:
        cmd = cmd.lower().strip()
        stem = self._stem
        if self._exception and self._exception_item['irregular']:
            dec_info = self._exception_item
            if cmd == 'noms':
                return _stem_ending_formatter(stem, dec_info['nom'], 0)
            elif cmd == 'nomp':
                return _stem_ending_formatter(stem, dec_info['nom'], 1)
            elif cmd == 'accs':
                return _stem_ending_formatter(stem, dec_info['acc'], 0)
            elif cmd == 'accp':
                return _stem_ending_formatter(stem, dec_info['acc'], 1)
            elif cmd == 'gens':
                return _stem_ending_formatter(stem, dec_info['gen'], 0)
            elif cmd == 'genp':
                return _stem_ending_formatter(stem, dec_info['gen'], 1)
            elif cmd == 'dats':
                return _stem_ending_formatter(stem, dec_info['dat'], 0)
            elif cmd == 'datp':
                return _stem_ending_formatter(stem, dec_info['dat'], 1)
            elif cmd == 'abls':
                return _stem_ending_formatter(stem, dec_info['abl'], 0)
            elif cmd == 'ablp':
                return _stem_ending_formatter(stem, dec_info['abl'], 1)
            elif cmd == 'vocs':
                return _stem_ending_formatter(stem, dec_info['voc'], 0)
            elif cmd == 'vocp':
                return _stem_ending_formatter(stem, dec_info['voc'], 1)
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
