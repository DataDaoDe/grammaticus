from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Dict, Any

from grammaticus.grammar import (
    Person,
    Number,
    Tense,
    Mood,
    Aspect
)


class Word:

    def __init__(self, lemma: str):
        self._lemma = lemma


class FirstConjugation:

    def __init__(self, stem: str):
        self._forms = {}
        self._stem = stem
        self._build()

    def get_forms(self) -> Dict[str, Any]:
        return self._forms

    def _build(self):
        forms = {
            'present': {
                'active': [],
                'passive': []
            },
            'future': {
                'active': [],
                'passive': []
            }
        }
        stem = self._stem

        # suffixes
        present_actives = ['o', 'as', 'at', 'amus', 'atis', 'ant']
        present_passives = ['or', 'aris', 'atur', 'amur', 'amini', 'antur']
        future_actives = ['abo', 'abis', 'abit', 'abimus', 'abitis', 'abunt']
        future_passives = ['abor', 'aberis',
                           'abitur', 'abimur', 'abimini', 'abuntur']
        for idx in range(0, 6):
            pa = '{}{}'.format(stem, present_actives[idx])
            pp = '{}{}'.format(stem, present_passives[idx])

            forms['present']['active'].append(pa)
            forms['present']['passive'].append(pp)

            fa = '{}{}'.format(stem, future_actives[idx])
            fp = '{}{}'.format(stem, future_passives[idx])

            forms['future']['active'].append(fa)
            forms['future']['passive'].append(fp)

        self._forms = forms


class Verb(Word):

    def __init__(self, lemma: str):
        super().__init__(lemma=lemma)
        self._conj = {}
        self._build_conjugations()

    def _build_conjugations(self):
        stem = self._lemma[:-1]
        # todo:  determine conjugation
        self._conj = FirstConjugation(stem)


class IQuery(BaseModel):
    person: Optional[Person]
    number: Optional[Number]
    tense: Optional[Tense]
    mood: Optional[Mood]
    aspect: Optional[Aspect]


class Query:

    def __init__(self, word: Word):
        self._w = word
        self._q = IQuery()

    def person(self, person: Person) -> Query:
        self._q.person = person
        return self

    def number(self, number: Number) -> Query:
        self._q.number = number
        return self

    def tense(self, tense: Tense) -> Query:
        self._q.tense = tense
        return self

    def mood(self, mood: Mood) -> Query:
        self._q.mood = mood
        return self

    def aspect(self, aspect: Aspect) -> Query:
        self._q.aspect = aspect
        return self

    def resolve(self) -> str:
        forms = self._w.forms()
