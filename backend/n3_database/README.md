# N3 Database Module

## API Functions

- `init_db()`: Initializes the local TinyDB database.
- `save_user_profile(profile: dict)`: Stores or updates a user profile.
- `save_location(loc: dict)`: Stores a location with its metadata and vectors.
- `get_all_locations() -> list[dict]`: Retrieves all stored locations.

## Data Schema

### Location Object
```python
{
    "location_id": str,
    "vectors": {
        "text": list[float],     # BGE-M3 (1024d)
        "aug_text": list[float], 
        "aug_tags": list[float],
        "img_desc": list[float]
    },
    "metadata": {
        "name": str,
        "description": str,
        "tags": list[str]
    },
    "geo": {
        "lat": float,
        "lng": float
    }
}
```

### User Profile Object
```python
{
    "user_id": str,
    "text": str,
    "tags": list[str],
    "img_desc": str,
    "vectors": dict, # N1 vector outputs
    "constraints": dict
}
```
