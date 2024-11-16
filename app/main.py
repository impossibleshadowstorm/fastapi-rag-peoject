from fastapi import FastAPI
from app.routes import auth, documents, queries

app = FastAPI(
    title="FastAPI RAG Project",
    description="A full-stack project for document management with RAG capabilities.",
    version="1.0.0"
)

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/documents", tags=["Document Management"])
app.include_router(queries.router, prefix="/query", tags=["NLP Query"])
