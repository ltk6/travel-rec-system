# N5: Activity Generation

Hybrid engine (Templates + LLM) to generate personalized activities for ranked locations.

## API
```python
generate_activities(data: dict) -> dict
```

### Input
- `user`: Preferences & tags
- `locations`: Output from N4
- `constraints`: Budget & Time limits

### Output
- `activities`: List of activities per location with cost, duration, and personalized reasoning.