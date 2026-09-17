import chromadb
from sentence_transformers import CrossEncoder, SentenceTransformer


_embed_model = None
_reranker = None

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

def get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    return _embed_model


def get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANK_MODEL_NAME)
    return _reranker