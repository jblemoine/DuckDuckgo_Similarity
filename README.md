# DuckDuckgo_Similarity

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

print(doc1.similarity(doc2))

```

# Test

```sh
pytest
```

