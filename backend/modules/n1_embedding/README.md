# Embedding Module

Provides a single public interface to convert user or location data into multi-channel embeddings.

## API

```python
embed(data: dict) -> dict
```

### Input

* `text`: raw text input
* `tags`: list of tag keys
* `image_description`: visual description

### Output

* `preprocessed`: normalized + expanded inputs
* `vectors`: embeddings for `text`, `aug_text`, `aug_tags`, `image_description`

## Responsibilities

* Build augmented inputs (text + tags)
* Generate embeddings via BGE-M3
* Return aligned multi-channel vectors for downstream comparison
