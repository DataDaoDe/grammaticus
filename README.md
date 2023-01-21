# Grammaticus

Grammaticus is a library of utility functions for working with language grammars.

I am currently working on supporting Latin.

## Example
```python
from grammaticus.languages.latin import nouns

agricol = nouns.get_stem('agricola') # => 'agricol'
forms = nouns.decline(agricol, declension=nouns.FIRST_DECLENSION) # returns a pandas DataFrame
print(forms['accusative']['plural']) # => 'agricolam'
```


## Todos

1. Latin: add support for nouns and verbs
2. Latin: add support for pronouns
3. Latin: add support for adjectives and adverbs
4. Latin: add support for irregular and rare forms