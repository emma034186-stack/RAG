from sentence_transformers import SentenceTransformer
import numpy as np

# 載入向量模型（推薦使用 BAAI/bge-m3）
def load_embedder(model_name="BAAI/bge-m3"):
    return SentenceTransformer(model_name)

# 將多個文字段落轉成向量陣列
def compute_embedding(embedder, texts):
    embeddings = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return np.array(embeddings)
