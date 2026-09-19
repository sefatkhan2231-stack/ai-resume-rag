
## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running locally, with the model pulled:
```bash
  ollama pull llama3.2
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App available at `http://localhost:5173`.

### Environment Variables

**Backend** (`backend/.env`):

| Variable | Default | Description |
|---|---|---|
| `FRONTEND_URL` | `http://localhost:5173` | Allowed CORS origin |
| `UPLOAD_DIR` | `./storage/uploads` | Where uploaded PDFs are saved |
| `VECTOR_DB_PATH` | `./storage/chroma` | ChromaDB persistence path |
| `DATABASE_PATH` | `./storage/app.db` | SQLite file path |
| `OLLAMA_MODEL` | `llama3.2` | Model used for assessment and requirement extraction |
| `OLLAMA_HOST` | *(unset = localhost:11434)* | Set this when Ollama runs elsewhere (e.g. a separate deployment) |

**Frontend** (`frontend/.env`):

| Variable | Default | Description |
|---|---|---|
| `VITE_API_URL` | `http://127.0.0.1:8000/api` | Backend API base URL |

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/resumes/upload` | Upload a single resume |
| POST | `/api/resumes/batch-upload` | Upload multiple resumes, per-file status |
| POST | `/api/resumes/rank` | Rank candidates against a job description |
| POST | `/api/jobs/analyze` | Extract structured requirements from a job description |
| POST | `/api/screening/analyze` | Single-candidate screening with full LLM assessment |
| POST | `/api/job-matching/analyze` | Full per-candidate LLM evaluation + evidence for multiple candidates |
| GET | `/api/dashboard/stats` | Resume/screening counts and average score |
| GET | `/api/dashboard/activity` | Daily screening counts for charting |
| GET | `/api/dashboard/history` | Past screening runs |
| GET | `/api/results/export/{screening_id}` | CSV export of a stored screening run |

Full interactive documentation is available at `/docs` once the backend is running.

## Deployment

Deployed on [Railway](https://railway.app):

- **Backend** — deployed directly from this repo (Nixpacks auto-detects Python, no Dockerfile needed)
- **Ollama** — deployed as a separate private service (no public domain — Ollama has no built-in auth), using Railway's [Ollama template](https://railway.com/deploy/ollama-private-llm-embeddings-api-on-railway)
- The backend reaches Ollama over Railway's private network via the `OLLAMA_HOST` environment variable — no code changes needed, since the `ollama` Python client reads it directly

## Known Limitations

- **No structured "years of experience" extraction** — the requirement extractor pulls skills/tools/frameworks/databases/soft-skills from a job description, not experience-level requirements. Ranking and CSV exports reflect this honestly rather than fabricating an experience-match figure.
- **Contact info extraction is heuristic** — name/email/phone are parsed with regex and a "first line of the resume" assumption, not guaranteed reliable across all resume formats.
- **No authentication** — this is a single-tenant portfolio project; anyone with access to the deployed URL can upload and screen resumes.
- **Ranking against the full candidate pool by default** — `/resumes/rank` and `/job-matching/analyze` score every stored candidate unless a specific `candidate_ids` list is passed (the frontend always scopes this to the resumes just uploaded in that session).

## Roadmap

- Browse/select from previously uploaded candidates without re-uploading
- Structured experience-requirement extraction and matching
- Authentication and multi-user support
- Background job processing for large batch uploads
