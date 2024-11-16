from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
    parsed = Column(Integer, default=0)

    # Optional content relationship to DocumentContent, no foreign key reference in this model
    content = relationship(
        "DocumentContent",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )
    owner = relationship("User")


class DocumentContent(Base):
    __tablename__ = "document_contents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    # content = Column(String, nullable=False)  # Could be JSON or plain text
    # document_metadata = Column(String, nullable=True)  # Optional metadata extracted
    content = Column(JSON, nullable=False)  # Use JSON type for content
    document_metadata = Column(JSON, nullable=False)  # Metadata also stored as JSON

    # Define the reverse relationship with Document
    document = relationship(
        "Document",
        back_populates="content",
    )
