import pandas as pd
from Duckduckgo_Similarity.engine import DdgToken


if __name__ == '__main__':
    pseudo = pd.read_csv('data/pseudonym.csv', names=['pseudo'])
    real_names = pd.read_csv('data/real_name.csv', names=['real_name'])

    score = pd.concat([pseudo, real_names], axis=1)

    score = pd.DataFrame(score, score.pseudo, score.real_name)

    # compute score matrix
    for pseudo in score.index:
        for name in score.columns:

            score.loc[pseudo, name] = DdgToken(pseudo).similarity(DdgToken(name), metric='mean') # try with metric='max'

    # export score matrix
    score.to_csv('data/score_matrix.csv')

    # export features
    all_features = pd.concat([pd.DataFrame(token.features, index=[token.string]) for token in DdgToken.get_instances()])
    all_features.to_csv('data/features.csv')