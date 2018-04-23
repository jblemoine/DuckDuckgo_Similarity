# DuckDuckgo_Similarity

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/jblemoine/DuckDuckgo_Similarity/master)
.. image:: https://mybinder.org/badge.svg :target: https://mybinder.org/v2/gh/jblemoine/DuckDuckgo_Similarity/master

Similarity engine using duckduckgo api

# Installation 

```sh

$pip install -r path/DuckDuckGo_Similarity/requirements.txt
$python -m spacy download en
```

# Usage 

```python

from Duckduckgo_Similarity.engine import DdgToken


# compute similarity score between two search query terms.

doc1 = DdgToken('the fries were gross')
doc2 = DdgToken('worst fries ever')

print(doc1.similarity(doc2,
                      metric='mean')) # allowed values : 'mean', 'max'.

```

# Test

```sh
pytest
```

