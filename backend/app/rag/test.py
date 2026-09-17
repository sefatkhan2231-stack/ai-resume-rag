from backend.app.rag.reranking import detect_section
from backend.app.resume.test_pdf import test_extract_pdf_text
from backend.app.rag.vector_store import index_chunks, reset_collection
from backend.app.rag.retrieval import retrieve_and_rerank

def test():

    chunks = test_extract_pdf_text()

    chunk_length = index_chunks(chunks, resume_id="resume_001", candidate_id="candidate_001")

    print(f"Indexed {chunk_length} chunks into Chroma collection.")

    queries = [
        "Does this candidate know React?",
        "Does this candidate know Python?",
        "Does this candidate know Laravel?",
        "Does this candidate have SQL experience?",
        "Does this candidate have Git and GitHub experience?",
    ]

    # collection = reset_collection()

    # print(f"Chroma collection reset. {collection}")

    for query in queries:

        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("=" * 70)

        results = retrieve_and_rerank(query,
            n_results=5,
            max_results=3
        )

        for i, result in enumerate(results, 1):
            print(f"\nRESULT {i}")
            print("RERANK SCORE:", result["rerank_score"])
            print("SECTION:", result["metadata"].get("section"))
            print("SUBSECTION:", result["metadata"].get("subsection"))
            print("DOCUMENT:")
            print(result["document"])
            print(query, "→", detect_section(query))

if __name__ == "__main__":
    test()