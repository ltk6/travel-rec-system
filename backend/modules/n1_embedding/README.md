# Embedding Module

Provides a single public interface to convert user or location data into multi-channel embeddings.

## API

```python
embed(data: dict) -> dict
```

### Input

* `text`: raw text input
* `tags`: list of tag keys
* `img_desc`: visual description

### Output

* `sig_k`: keyword expansion count, determine weighting of each vector
* `preprocessed`: normalized + expanded inputs with keys:
  * `text`: raw text input
  * `aug_text`: expanded text input
  * `aug_tags`: expanded tag input
  * `img_desc`: visual description
* `vectors`: embeddings for `text`, `aug_text`, `aug_tags`, `img_desc`

## Responsibilities

* Build augmented inputs (text + tags)
* Generate embeddings via BGE-M3
* Return aligned multi-channel vectors for downstream comparison
