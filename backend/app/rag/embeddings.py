import os
import numpy as np
import chromadb
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

_embed_model = None
_reranker = None

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL_NAME = "Xenova/ms-marco-MiniLM-L-6-v2"

# Keep downloaded models on the Railway volume so they survive redeploys
CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "/data/models")


class _Embedder:
    def __init__(self):
        self._m = TextEmbedding(model_name=EMBED_MODEL_NAME, cache_dir=CACHE_DIR)

    def encode(self, texts, **kwargs):
        single = isinstance(texts, str)
        if single:
            texts = [texts]
        vecs = np.array(list(self._m.embed(texts)))
        return vecs[0] if single else vecs


class _Reranker:
    def __init__(self):
        self._m = TextCrossEncoder(model_name=RERANK_MODEL_NAME, cache_dir=CACHE_DIR)

    def predict(self, pairs, **kwargs):
        # pairs: [(query, passage), ...], same as CrossEncoder.predict
        if not pairs:
            return np.array([])
        query = pairs[0][0]
        if all(p[0] == query for p in pairs):
            return np.array(list(self._m.rerank(query, [p[1] for p in pairs])))
        return np.array([next(iter(self._m.rerank(q, [d]))) for q, d in pairs])


def get_embed_model() -> _Embedder:
    global _embed_model
    if _embed_model is None:
        _embed_model = _Embedder()
    return _embed_model


def get_reranker() -> _Reranker:
    global _reranker
    if _reranker is None:
        _reranker = _Reranker()
    return _reranker