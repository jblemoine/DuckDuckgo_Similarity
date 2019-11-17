# DuckDuckgo_Similarity

Similarity engine using duckduckgo api

# Installation 

```sh

$pip install -r requirements.txt
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

