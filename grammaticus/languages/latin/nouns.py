from typing import Optional, List, Any
import pandas as pd


class Noun:

    def __init__(self, stem, gender, declension, meta=None):
        self._stem = stem
        self._gender = gender
        self._declension = declension
        self._meta = meta

    def stem(self):
        return self._stem

    def gender(self):
        return self._gender

    def declension(self):
        return self._declension

    def __repr__(self):
        return '<{} [{}:{}]>'.format(self._stem, self._gender, self._declension)


CASES = ['nominative', 'genitive', 'dative',
         'accusative', 'ablative', 'vocative']

FIRST_DECLENSION = pd.DataFrame({
    'nominative': ['a', 'ae'],
    'genitive': ['ae', 'arum'],
    'dative': ['ae', 'is'],
    'accusative': ['am', 'as'],
    'ablative': ['a', 'is'],
    'vocative': ['a', 'ae'],
}, index=['singular', 'plural'])

SECOND_DECLENSION_MASCULINE = pd.DataFrame({
    'nominative': ['us', 'i'],
    'genitive': ['i', 'orum'],
    'dative': ['o', 'is'],
    'accusative': ['um', 'os'],
    'ablative': ['o', 'is'],
    'vocative': ['e', 'i'],
}, index=['singular', 'plural'])

SECOND_DECLENSION_NEUTER = pd.DataFrame({
    'nominative': ['um', 'a'],
    'genitive': ['i', 'orum'],
    'dative': ['o', 'is'],
    'accusative': ['um', 'a'],
    'ablative': ['o', 'is'],
    'vocative': ['um', 'a'],
}, index=['singular', 'plural'])


IR_ENDINGS = ['vir']
ER_ENDINGS_E_KEEPERS = ['armiger', 'puer', 'adulter', 'socer',
                        'gener', 'vesper', 'lucifer', 'signifer']
ER_ENDINGS_E_LOSERS = ['aper:apr', 'arbiter:arbitr', 'cancer:cancr', 'caper:capr',
                       'culter:cultr', 'fiber:fibr', 'magister:magistr', 'faber:fabr', 'ager:agr', 'liber:libr', 'minister:ministr']


def extract_second_declension_stem(word: str) -> Optional[str]:

    if word == 'vir':
        # only ir ending 2nd declension word, stem is also `vir`
        return word

    # handle er words
    for er_keeper in ER_ENDINGS_E_KEEPERS:
        if word.startswith(er_keeper):
            # we have an -er keeper of the 2nd declension
            return er_keeper
    for er_loser in ER_ENDINGS_E_LOSERS:
        er, r = er_loser.split(':')
        if word == er:
            return word
        if word.startswith(r):
            return r

    # handle masculine
    m_endings = sorted(SECOND_DECLENSION_MASCULINE.to_numpy().ravel(),
                       key=len, reverse=True)

    for m_end in m_endings:
        if word.endswith(m_end):
            stem = word[:(word.rindex(m_end))]
            return stem

    # handle neuter
    n_endings = sorted(SECOND_DECLENSION_NEUTER.to_numpy().ravel(),
                       key=len, reverse=True)

    for n_end in n_endings:
        if word.endswith(n_end):
            stem = word[:(word.rindex(n_end))]
            return stem


def extract_first_declension_stem(word: str) -> Optional[List[Any]]:
    endings = sorted(FIRST_DECLENSION.to_numpy().ravel(),
                     key=len, reverse=True)

    # start with longest
    for end in endings:
        if word.endswith(end):
            stem = word[:(word.rindex(end))]
            return stem


def decline(stem: str, declension) -> pd.DataFrame:

    forms = declension.copy(deep=True)
    for case in CASES:
        forms[case] = forms[case].apply(
            lambda x: '{}{}'.format(stem, x))

    return forms


def word_ending(word: str, stem: str) -> str:
    if len(word) < len(stem):
        raise ValueError(
            'word length must be greater than or equal to stem length.')
    return word[len(stem):]


def first_declension_cases_with_ending(ending: str) -> List[Any]:
    cases = FIRST_DECLENSION[FIRST_DECLENSION.isin([ending])]
    matching_cases = []
    for row_key, row in cases.iterrows():
        for case_name in CASES:
            value = row[case_name]
            if pd.isna(value) or pd.isnull(value):
                continue
            else:
                matching_cases.append((row_key, case_name))
    return matching_cases


def first_declension_to_singular(plural_noun: str, case: str = None):
    stem = extract_first_declension_stem(plural_noun)
    if case:
        return '{}{}'.format(stem, FIRST_DECLENSION[case]['singular'])
    else:
        ending = word_ending(plural_noun, stem)
        case_info = first_declension_cases_with_ending(ending)
        plural_case_matches = list(
            filter(lambda x: x[0] == 'plural', case_info))
        if len(plural_case_matches) > 0:
            first_match = plural_case_matches[0]
            return '{}{}'.format(stem, FIRST_DECLENSION[first_match[1]]['singular'])


def first_declension_to_plural(singular_noun: str, case: str = None):
    stem = extract_first_declension_stem(singular_noun)
    if case:
        return '{}{}'.format(stem, FIRST_DECLENSION[case]['plural'])
    else:
        ending = word_ending(singular_noun, stem)
        case_info = first_declension_cases_with_ending(ending)
        singular_case_matches = list(
            filter(lambda x: x[0] == 'singular', case_info))
        if len(singular_case_matches) > 0:
            first_match = singular_case_matches[0]
            return '{}{}'.format(stem, FIRST_DECLENSION[first_match[1]]['plural'])
