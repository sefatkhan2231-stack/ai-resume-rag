from app.rag.embeddings import get_embed_model, get_reranker
from app.rag.vector_store import get_collection

def search_resume(query: str, n_results: int = 3, section: str = None, candidate_id: str = None) -> dict:
    model = get_embed_model()
    collection = get_collection()

    query_embedding = model.encode(query).tolist()
    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"],
    }

    condition = []
    if section:
        condition.append({"section": section})
    if candidate_id:
        condition.append({"candidate_id": candidate_id})

    if len(condition) == 1:
        kwargs["where"] = condition[0]
    elif len(condition) > 1:
        kwargs["where"] = {"$and": condition}

    return collection.query(**kwargs)


def detect_section(query: str):
    q = query.lower()
    if any(w in q for w in ["project", "projects", "built", "application", "app"]):
        return "PROJECTS"
    if any(w in q for w in ["work", "worked", "experience", "job", "company", "internship"]):
        return "PROFESSIONAL EXPERIENCE"
    if any(w in q for w in ["education", "study", "studied", "college", "school", "degree", "training"]):
        return "EDUCATION"
    if any(w in q for w in ["skill", "skills", "know", "database", "language", "framework", "tool"]):
        return "SKILLS"
    return None


def rerank_results(query: str, results: dict) -> list:
    documents = results["documents"][0]
    if not documents:
        return []

    reranker = get_reranker()
    pairs = [[query, doc] for doc in documents]
    scores = reranker.predict(pairs)

    ranked = [
        {
            "document": documents[i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
            "rerank_score": float(scores[i]),
        }
        for i in range(len(documents))
    ]
    ranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return ranked