from Duckduckgo_Similarity.engine import extract_feature, DdgToken


def test_extract_feature():

    features = extract_feature('Duckduckgo')

    for feature in features:
        assert features[feature]


def test_DdgToken():
    assert DdgToken('marshall bruce mathers').similarity(DdgToken('Eminem')) == 1.0
