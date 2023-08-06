# NLIGraphSpacy
Knowledge graph using NLP Spacy

## Installation

```python
pip install nligraphspacy
```

## Implementation

```python
from nligraphspacy import NLIGRAPH
nligraph = NLIGRAPH.RelationEntityExtract("She worked in the city of London")
nligraph.process_text()
# ('She', 'worked', 'London')
```
