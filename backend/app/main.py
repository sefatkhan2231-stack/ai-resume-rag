

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.api.routes import health, resumes, jobs, screening, dashboard, job_matching, results
from app.rag.embeddings import get_embed_model, get_reranker
from app.rag.vector_store import get_collection

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_embed_model()
    get_reranker()
    get_collection()
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(health.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(screening.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(job_matching.router, prefix="/api")
app.include_router(results.router, prefix="/api")
