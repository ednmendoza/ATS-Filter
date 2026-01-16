from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .db import Base


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    parsed_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String, nullable=False)  # linkedin, indeed, dice
    raw_text = Column(Text, nullable=False)
    extracted_signals = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ResumeVariant(Base):
    __tablename__ = "resume_variants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False, index=True)
    jd_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False, index=True)
    persona = Column(String, nullable=False)  # ic, architect, hybrid
    platform = Column(String, nullable=False)  # linkedin, indeed, dice
    compiled_text = Column(Text, nullable=False)
    scores = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApplicationOutcome(Base):
    __tablename__ = "application_outcomes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("resume_variants.id"), nullable=False, index=True)
    status = Column(String, nullable=False)  # rejected, interview, ghosted
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
