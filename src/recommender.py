import json
import numpy as np
from datetime import date
from .nlp import ALL_TAGS

# load data
def load_locations():
    with open("data/locations.json", encoding="utf-8") as f:
        return json.load(f)

# vector hóa
def vectorize(tags):
    v = np.zeros(len(ALL_TAGS))
    for t in tags:
        if t in ALL_TAGS:
            v[ALL_TAGS.index(t)] = 1
    return v

# cosine similarity
def cosine_sim(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# seasonal score
def seasonal_score(loc):
    month = date.today().month
    return 1.0 if month in loc["best_months"] else 0.5

# final score
def final_score(loc, user_vec):
    loc_vec = vectorize(loc["tags"])

    sim = cosine_sim(user_vec, loc_vec)
    seasonal = seasonal_score(loc)
    popularity = loc.get("popularity", 0.5)

    return round(
        0.60 * sim +
        0.25 * seasonal +
        0.15 * popularity,
        4
    )

# recommend
def recommend(user_tags, top_k=5):
    user_vec = vectorize(user_tags)
    locations = load_locations()

    scored = []
    for loc in locations:
        score = final_score(loc, user_vec)
        scored.append({**loc, "score": score})

    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]