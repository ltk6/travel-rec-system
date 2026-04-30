# Image Processing Module

Provides a vision-to-semantic layer that converts image data into descriptive text for travel recommendation.

## API

```python
process_image(data: dict) -> dict
```

### Input

* `image`: raw image data in bytes

### Output

* `img_desc`: a concise Vietnamese description (2-3 sentences) focusing on:
  * Location type (beach, temple, cafe, etc.)
  * Architecture or landscape (modern, ancient, primeval forest, etc.)
  * Atmosphere (peaceful, bustling, majestic, cozy, etc.)
* `error`: error message (present only if processing fails)

## Responsibilities

* Preprocess raw image bytes for visual analysis
* Extract semantic travel features using Gemini Vision
* Filter out non-travel noise (e.g., people's clothing, license plates)
* Ensure descriptions are optimized for downstream embedding and ranking
