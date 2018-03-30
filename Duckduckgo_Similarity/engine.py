import spacy
from json.decoder import JSONDecodeError
from .duckduckgo import duckduckgo


def extract_feature(strg: str):
    r = duckduckgo.query(strg)

    features = {
        'abstract_text': r.abstract.text,
        'abstract_url': r.abstract.url,
        'image_url': r.image.url,
        'best_result': ''
    }

    try:
        features['best_result'] = duckduckgo.get_zci(strg)
    # handling of unknown error
    except JSONDecodeError:
        pass

    return features


class DdgToken:
    """
    A Duckduckgo Search instance.
    """

    nlp = spacy.load('en')
    _instances = []

    def __init__(self, string):

        self.string = string
        self.features = extract_feature(self.string)
        self._instances.append(self)

    @classmethod
    def get_instances(cls):
        return cls._instances

    @property
    def processed_features(self):

        nlp = self.nlp

        processed_features = {
            key: nlp(value) for key, value in self.features.items()
        }
        return processed_features

    def similarity(self, token, metric='mean'):
        """
        Compute a semantic similarity estimate over object's features. Defaults to cosine over vectors.

        :param token:
        :param metric: operation to perform over the feature similarity scores. Either 'max' or 'mean'. Default 'mean'.
        :type token: DdgToken
        :type metric: str
        :return: Similarity metric between two Duckduckgo research.
        :rtype: float
        """

        allowed_metrics = ['mean', 'max']
        if metric not in allowed_metrics:
            raise ValueError('metric must be either {}.'.format(' ,'.join(allowed_metrics)))

        similarities = {
            name: self.processed_features[name].similarity(token.processed_features[name]) for name in
            self.processed_features
        }
        values = similarities.values()

        if metric == 'mean':
            return sum(values) / len(values)

        elif metric == 'max':
            return max(values)





