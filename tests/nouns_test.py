import grammaticus.languages.latin.nouns as nouns


def test_extract_first_declension_info():
    # form : stem
    tests = [
        ['puellam', 'puell'],
        ['mensae', 'mens'],
        ['poeta', 'poet'],
        ['terra', 'terr'],
        ['poetis', 'poet'],
        ['aguarum', 'agu'],
        ['lunas', 'lun'],
    ]
    for t in tests:
        t_stem = t[1]
        t_form = nouns.extract_first_declension_stem(t[0])
        assert t_form == t_stem


def test_decline_for_first_declension():
    res = nouns.decline('agu', nouns.FIRST_DECLENSION)
    assert res['nominative']['singular'] == 'agua'
    assert res['nominative']['plural'] == 'aguae'
    assert res['genitive']['singular'] == 'aguae'
    assert res['genitive']['plural'] == 'aguarum'
    assert res['dative']['singular'] == 'aguae'
    assert res['dative']['plural'] == 'aguis'
    assert res['accusative']['singular'] == 'aguam'
    assert res['accusative']['plural'] == 'aguas'
    assert res['ablative']['singular'] == 'agua'
    assert res['ablative']['plural'] == 'aguis'
    assert res['vocative']['singular'] == 'agua'
    assert res['vocative']['plural'] == 'aguae'
