import spacy
from json.decoder import JSONDecodeError
from googletrans import Translator
from .duckduckgo import duckduckgo


def extract_feature(strg: str):

    # pick the best language between french and english
    r = duckduckgo.query(strg)

    if r.abstract.text:

        features = {
            'abstract_text': r.abstract.text,
            'abstract_url': r.abstract.url.split('/')[-1],
            'image_url': r.image.url.split('/')[-1],
            'best_result': '',
        }

    # if nothing found in english get the french version and translate in english
    else:
        r = duckduckgo.query(strg, kad='fr_Fr')
        tr = Translator()

        features = {
            'abstract_text': tr.translate(r.abstract.text, dest='en').text,
            'abstract_url': r.abstract.url.split('/')[-1],
            'image_url': r.image.url.split('/')[-1],
            'best_result': '',

        }

    if not features['abstract_text']:
        try:
            features['best_result'] = duckduckgo.get_zci(strg)
        except JSONDecodeError:
            pass

    return features


class DdgToken:
    """
    A Duckduckgo Search instance.
    """

    nlp = spacy.load('en')
    _instances = []
    _instances_string = []

    def __init__(self, string):

        self.string = string
        self.features = extract_feature(self.string)

        if self.string not in DdgToken._instances_string:
            DdgToken._instances.append(self)
            DdgToken._instances_string.append(self.string)

    @classmethod
    def get_instances(cls):

        instances = cls._instances
        cls._instances = []
        cls._instances_string = []
        return instances

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

        values = [self.processed_features[name].similarity(token.processed_features[name]) for name in
                  self.processed_features if (self.processed_features[name] and token.processed_features[name])
                  ]

        # I add those metrics, since the artist name of pseudonym tend to be found among abstract_text or abstract_url.
        values.extend(
            [self.nlp(self.string).similarity(token.processed_features[name])
             for name in ['abstract_text', 'abstract_url']])

        values.extend(
            [self.nlp(token.string).similarity(self.processed_features[name])
             for name in ['abstract_text', 'abstract_url']])

        if metric == 'mean':
            return sum(values) / len(values)

        elif metric == 'max':
            return max(values)





