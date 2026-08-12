import faiss
import numpy as np
import json  # ✅ 加入 json 模組

def load_vector_store(index_path="vector_store.faiss", meta_path="doc_chunks.json"):
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:  # ✅ 改為 JSON 讀取
        metadata = json.load(f)
    return index, metadata

def retrieve_top_k(query_vector, index, metadata, top_k=3):
    scores, indices = index.search(np.array([query_vector]).astype("float32"), top_k)
    results = [metadata[i] for i in indices[0] if i != -1]
    return results
