# N4 Ranking — Channel Weighting Guide

---

## The 4 Active Channels

| Channel    | Representation         | Role                                  |
| ---------- | ---------------------- | ------------------------------------- |
| `text`     | Raw user input         | High-precision, literal intent        |
| `aug_text` | Expanded semantic text | Contextual + emotional interpretation |
| `aug_tags` | Expanded tag strings   | Stable semantic anchor                |
| `image`    | Image description      | Visual alignment                      |

`text` and `aug_text` are both needed and genuinely different:
- `text` captures **what the user literally said** — high precision for detailed input
- `aug_text` expansions are long descriptive sentences that **reframe emotional/contextual
  language into travel vocabulary** — powerful for vague input, but their verbosity
  can drown out precise intent when text is already rich

---

## Channel Weights

The system dynamically adjusts channel contributions based on **sig_k**.

`sig_k` is the **keyword expansion count** extracted from `text` during preprocessing.  
It measures how much semantic enrichment was required to understand the input.

- Low `sig_k` → input is weak with low keyword count
- High `sig_k` → input is already rich with high keyword count

## Base Channel Weights

All inputs start from a neutral baseline:
| text | tags | image|
|------|------|------|
|0.4  | 0.4  | 0.2   |

## sig_k-based Channel Weighting
| sig_k | text | aug_text | aug_tags | img_desc | reasoning |
|-------|------|----------|----------|----------|----------|
| 0  | 0.3 | 0.0 | 0.5 | 0.2 | aug_text is meaningless, text is also probably weak, slight boost to aug_tags |
| 1  | 0.1 | 0.3 | 0.4 | 0.2 | aug_text has 1 expansion, and probably is a lot stronger than text at this point |
| 2  | 0.2 | 0.2 | 0.4 | 0.2 | aug_text has 2 expansion and remain balanced |
| 3+ | 0.3 | 0.1 | 0.4 | 0.2 | aug_text rapidly loose value due to high expansion count |