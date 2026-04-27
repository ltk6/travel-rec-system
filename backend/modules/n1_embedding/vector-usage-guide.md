# N4 Ranking — Channel Weighting Guide

---

## The 4 Active Channels

| Channel    | Representation         | Role                                  |
| ---------- | ---------------------- | ------------------------------------- |
| `text`     | Raw user input         | High-precision, literal intent        |
| `aug_text` | Expanded semantic text | Contextual + emotional interpretation |
| `aug_tags` | Expanded tag strings   | Stable semantic anchor                |
| `image`    | Image description      | Visual alignment (supplementary)      |

`text` and `aug_text` are both needed and genuinely different:
- `text` captures **what the user literally said** — high precision for detailed input
- `aug_text` expansions are long descriptive sentences that **reframe emotional/contextual
  language into travel vocabulary** — powerful for vague input, but their verbosity
  can drown out precise intent when text is already rich

---

## Text Quality Score

The system should dynamically adjusts how much each channel contributes based on **text quality**.

```python
def score_text_quality(text: str) -> float:
    """0.0 = vague/empty, 1.0 = rich and specific. Saturates at 30 words."""
    if not text or not text.strip():
        return 0.0
    return min(len(text.split()) / 30, 1.0)
```

---

## Channel Weights

As text quality rises:
- `text` gains weight — user said something precise, trust it
- `aug_text` loses weight — expansions risk overwriting specific intent with generic travel vocabulary
- `aug_tags` recedes to anchor role
- `image` fades to near-irrelevant

| Input Quality   | System Behavior                                   |
| --------------- | ------------------------------------------------- |
| Low (vague)     | Relies on `aug_text` + `aug_tags` to infer intent |
| Medium          | Balanced interpretation across channels           |
| High (detailed) | Prioritizes `text`, reduces expansion influence   |

---