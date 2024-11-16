from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import DocumentContent
from app.utils.query_handler import handle_query
from app.utils.elastic_search_client import search_document_content

router = APIRouter()


@router.post("/")
def query_document(
    document_id: int,
    query: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    document_content = (
        db.query(DocumentContent)
        .filter(DocumentContent.document_id == document_id)
        .first()
    )

    if not document_content:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Pass the content and query to the RAG agent for processing
    response = handle_query(document_content.content, query)

    if not response:
        raise HTTPException(status_code=404, detail="No relevant data found.")
    
    return {"response": response}