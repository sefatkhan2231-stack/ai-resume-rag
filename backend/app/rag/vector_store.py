import chromadb

from app.rag.embeddings import get_embed_model

_collection = None

CHROMA_PATH = "../dataset/chroma"
COLLECTION_NAME = "resume_chunk_v2"

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def build_metadata(chunk: dict, resume_id: str, candidate_id: str) -> dict:
    metadata = {"resume_id": resume_id, "candidate_id": candidate_id, "section": chunk["section"]}
    for key in ("subsection", "project", "job_title", "company"):
        if key in chunk:
            metadata[key] = chunk[key]
    return metadata


def index_chunks(chunks: list, resume_id: str = "resume_001", candidate_id: str = "candidate_001"):
    """Embed a list of {"text": ..., "section": ..., ...} chunks and add to Chroma."""
    model = get_embed_model()
    collection = get_collection()

    documents = [c["text"] for c in chunks]
    embeddings = model.encode(documents)
    ids = [f"{resume_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [build_metadata(c, resume_id, candidate_id) for c in chunks]

    collection.upsert(ids=ids, documents=documents, embeddings=embeddings.tolist(), metadatas=metadatas)
    return len(chunks)


def reset_collection():

    global _collection

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Old collection deleted.")
    except Exception:
        print("No old collection found.")

    _collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print("New collection created.")

    return _collection