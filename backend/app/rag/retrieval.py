from app.rag.reranking import search_resume, detect_section, rerank_results

RERANK_THRESHOLD = -10.3

def retrieve_and_rerank(query: str, candidate_id: str = None, n_results: int = 10, max_results: int = 3,
                         threshold: float = RERANK_THRESHOLD) -> list:
    section = detect_section(query)
    results = search_resume(query=query, n_results=n_results, section=section, candidate_id=candidate_id)
    ranked = rerank_results(query, results)
    relevant = [r for r in ranked if r["rerank_score"] >= threshold]
    return relevant[:max_results]