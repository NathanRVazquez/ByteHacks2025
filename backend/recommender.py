import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import pickle
import numpy as np

df = pd.read_csv('data.csv')
df = df.fillna("")

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

tag_index = faiss.read_index("faiss-t.index")
with open("faiss-t.pkl", "rb") as f:
    tag_events = pickle.load(f)

description_index = faiss.read_index("faiss_d.index")

# returns top 10 as a list of dicts
def recommend_tags(user_tags):
    user_embedding = model.encode([" | ".join(user_tags)], convert_to_numpy=True)
    distances, indices = tag_index.search(user_embedding, k=10)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "event_id": int(df.iloc[int(idx)]["event_id"]),  # ensure int
            "similarity_score": float(dist)  # ensure float
        })
    return results

def recommend_description(event_description):
    query_emb = model.encode([event_description], convert_to_tensor=False)
    query_emb = np.array(query_emb, dtype=np.float32)
    faiss.normalize_L2(query_emb)

    distances, indices = description_index.search(query_emb, 3)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "event_id": int(df.iloc[idx]["event_id"]),
            "similarity_score": float(dist)  # higher = more similar
        })
    
    return results