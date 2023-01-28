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

    def decline(cmd: str) -> str:
        raise Exception('implement')
