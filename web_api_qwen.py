
from flask import Flask, request, jsonify
from llama_cpp import Llama
from rag.embedder import load_embedder, compute_embedding
from rag.retriever import load_vector_store, retrieve_top_k
import os, json
import numpy as np
import fitz  # PyMuPDF

app = Flask(__name__)

llm = Llama(model_path="models/qwen1_5-0_5b-chat-q4_k_m.gguf", n_ctx=2048, n_threads=8, chat_format="chatml")
embedder = load_embedder("BAAI/bge-m3")

# ========== 向量查詢 ==========
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    query = data.get("query", "")
    query_vec = compute_embedding(embedder, [query])[0]
    index, metadata = load_vector_store("vector_store.faiss", "doc_chunks.json")
    results = retrieve_top_k(query_vec, index, metadata, top_k=3)

    context_text = "\n---\n".join(results)
    messages = [
        {"role": "system", "content": "你是中文法規助手，請根據提供內容回答。"},
        {"role": "user", "content": f"📚 文件內容如下：\n{context_text}\n\n🤔 問題：{query}"}
    ]
    res = llm.create_chat_completion(messages=messages)
    return jsonify({"answer": res["choices"][0]["message"]["content"]})


# ========== 建立向量庫 ==========
@app.route("/build", methods=["POST"])
def build_db():
    from sentence_transformers.util import cos_sim
    import faiss
    import pickle

    # 支援 .pdf 轉文字
    def extract_text(filepath):
        if filepath.endswith(".pdf"):
            doc = fitz.open(filepath)
            return "\n".join([page.get_text() for page in doc])
        elif filepath.endswith(".txt") or filepath.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    chunks = []
    for fname in os.listdir("docs"):
        if fname.endswith((".pdf", ".txt", ".md")):
            fullpath = os.path.join("docs", fname)
            text = extract_text(fullpath)
            # 分段 chunk，這裡簡單每 300 字一段
            chunks += [text[i:i+300] for i in range(0, len(text), 300)]

    embeddings = compute_embedding(embedder, chunks)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, "vector_store.faiss")

    with open("doc_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return jsonify({"message": f"✅ 已建庫，共 {len(chunks)} 筆段落"})
if __name__ == "__main__":
    app.run(debug=True)

