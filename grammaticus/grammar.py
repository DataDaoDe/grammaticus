from enum import Enum
from typing import Literal

from pydantic import BaseModel


class Person(str, Enum):
    first = 'first'
    second = 'second'
    third = 'third'


class Number(str, Enum):
    singular = 'singular'
    plural = 'plural'


class Gender(str, Enum):
    masculine = 'masculine'
    feminine = 'feminine'
    neuter = 'neuter'


class Tense(str, Enum):
    present = 'present'
    imperfect = 'imperfect'
    perfect = 'perfect'
    past = 'past'
    preterite = 'preterite'
    future = 'future'


class Mood(str, Enum):
    indicative = 'indicative'
    subjunctive = 'subjunctive'
    conditional = 'conditional'
    imperative = 'imperative'


class Aspect(str, Enum):
    simple = 'simple'
    perfect = 'perfect'
    continuous = 'continuous'


def is_realis(mood: str) -> bool:
    return mood == Mood.indicative


def is_irrealis(mood: Mood) -> bool:
    return not is_realis(mood)
