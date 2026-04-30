# Location Ranking Module

Ranks travel locations using weighted multi-channel cosine similarity between user and location vectors.

## API

```python
rank_locations(data: dict) -> dict
```

### Input

* `sig_k`: keyword expansion count (determines channel weights)
* `user_vectors`: embeddings from N1 (`text`, `aug_text`, `aug_tags`, `img_desc`)
* `locations`: list of locations with `location_vectors` (`text`, `tag`)
* `top_k`: number of locations to return

### Output

* `locations`: sorted list of ranked results:
  * `location_id`: unique identifier
  * `score`: final similarity score, normalized so the top result is 1.0
  * `reason`: Vietnamese explanation of why this location was recommended

## Responsibilities

* Resolve dynamic scoring weights based on `sig_k`
* Compute weighted cosine similarity across multiple vector channels
* Sort and prune results to return the top K recommendations
