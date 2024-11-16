from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import Document, DocumentContent
from app.utils.unstructured_client import process_document
from datetime import datetime
import os
import shutil
from app.utils.elastic_search_client import index_document


UPLOAD_DIR = "uploads/"
PROCESSED_DIR = "processed/"

router = APIRouter()


@router.post("/upload")
def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # Ensure directories exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Save file locally
    file_path = "/app/" + os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Store document metadata in the database
    new_document = Document(
        user_id=current_user.user_id,
        file_name=file.filename,
        file_url=file_path,
        uploaded_at=datetime.utcnow(),
    )
    db.add(new_document)
    db.commit()

    # Process the file using Unstructured API
    try:
        parsed_content = process_document()
        content_entry = DocumentContent(
            document_id=new_document.id,
            content=parsed_content["content"],
            document_metadata=parsed_content["metadata"],
        )
        db.add(content_entry)
        new_document.parsed = 1
        db.commit()

        # Index parsed content into Elasticsearch
        index_document(new_document.id, parsed_content["content"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    return {
        "message": "File uploaded and processed successfully",
        "file_url": file_path,
    }


@router.get("/")
def list_documents(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    documents = (
        db.query(Document).filter(Document.user_id == current_user.user_id).all()
    )
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found.")
    return {"documents": documents}
