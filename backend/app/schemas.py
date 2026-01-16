from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class ResumeUpload(BaseModel):
    user_id: str


class ResumeResponse(BaseModel):
    id: UUID
    user_id: str
    raw_text: str
    parsed_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobDescriptionCreate(BaseModel):
    platform: str  # linkedin, indeed, dice
    raw_text: str


class JobDescriptionResponse(BaseModel):
    id: UUID
    platform: str
    raw_text: str
    extracted_signals: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CompileVariantRequest(BaseModel):
    resume_id: UUID
    jd_id: UUID
    persona: str  # ic, architect, hybrid
    platform: str  # linkedin, indeed, dice


class SurvivabilityScores(BaseModel):
    keyword_score: float
    title_score: float
    age_proxy_risk: float
    overqual_risk: float
    survivability: float


class ResumeVariantResponse(BaseModel):
    id: UUID
    resume_id: UUID
    jd_id: UUID
    persona: str
    platform: str
    compiled_text: str
    scores: Optional[SurvivabilityScores] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class OutcomeCreate(BaseModel):
    variant_id: UUID
    status: str  # rejected, interview, ghosted


class OutcomeResponse(BaseModel):
    id: UUID
    variant_id: UUID
    status: str
    recorded_at: datetime
    
    class Config:
        from_attributes = True
