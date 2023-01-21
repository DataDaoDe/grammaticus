from typing import Optional, List, Any
import pandas as pd

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


def extract_first_declension_info(word: str) -> Optional[List[Any]]:
    endings = sorted(FIRST_DECLENSION.to_numpy().ravel(),
                     key=len, reverse=True)

    # start with longest
    for end in endings:
        if word.endswith(end):
            stem = word[:(word.rindex(end))]
            cases = FIRST_DECLENSION[FIRST_DECLENSION.isin([end])]
            matching_cases = []
            for row_key, row in cases.iterrows():
                for case_name in CASES:
                    value = row[case_name]
                    if pd.isna(value) or pd.isnull(value):
                        continue
                    else:
                        matching_cases.append((row_key, case_name))

            return [stem, matching_cases]


def decline(stem: str, declension) -> pd.DataFrame:

    forms = declension.copy(deep=True)
    for case in CASES:
        forms[case] = forms[case].apply(
            lambda x: '{}{}'.format(stem, x))

    return forms


def first_declension_to_singular(plural_noun: str):
    stem, case_info = extract_first_declension_info(plural_noun)
