from fastapi import FastAPI
from pydantic import BaseModel
from src.nlp import extract_tags
from src.recommender import recommend

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
class Query(BaseModel):
    text: str
    top_k: int = 5

@app.post("/recommend")
def get_recommend(q: Query):
    tags = extract_tags(q.text)
    results = recommend(tags, q.top_k)

    return {
        "tags": tags,
        "results": results
    }