from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uuid

from .db import Base, engine, get_db
from .models import Resume, JobDescription, ResumeVariant, ApplicationOutcome
from .schemas import (
    ResumeResponse,
    ResumeUpload,
    JobDescriptionCreate,
    JobDescriptionResponse,
    CompileVariantRequest,
    ResumeVariantResponse,
    OutcomeCreate,
    OutcomeResponse
)
from .parsing import parse_resume
from .jd_extract import extract_jd_signals
from .compiler import compile_resume_variant
from .scoring import calculate_survivability_score
from .config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="ATS-Aware Resume Compiler API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "ATS Resume Compiler API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/resumes/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form("default_user"),  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """Upload and parse a resume file"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Read file content
    try:
        file_content = await file.read()
        if not file_content or len(file_content) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Parse resume
    try:
        parsed_data = parse_resume(file_content, file.filename or "unknown")
        if not parsed_data.get("raw_text") or len(parsed_data["raw_text"].strip()) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from file. Please ensure the file is a valid PDF, DOCX, or TXT file.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
    
    # Save to database
    try:
        resume = Resume(
            user_id=user_id,
            raw_text=parsed_data["raw_text"],
            parsed_json=parsed_data.get("parsed_json")
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving resume: {str(e)}")


@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a resume by ID"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@app.get("/resumes", response_model=List[ResumeResponse])
async def list_resumes(
    user_id: str = "default_user",  # TODO: Get from auth
    db: Session = Depends(get_db)
):
    """List all resumes for a user"""
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    return resumes


@app.post("/jds", response_model=JobDescriptionResponse)
async def create_job_description(
    jd: JobDescriptionCreate,
    db: Session = Depends(get_db)
):
    """Create a job description and extract signals"""
    # Validate platform
    valid_platforms = ["linkedin", "indeed", "dice"]
    if jd.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Platform must be one of: {', '.join(valid_platforms)}"
        )
    
    # Extract signals
    extracted_signals = extract_jd_signals(jd.raw_text)
    
    # Save to database
    job_desc = JobDescription(
        platform=jd.platform.lower(),
        raw_text=jd.raw_text,
        extracted_signals=extracted_signals
    )
    db.add(job_desc)
    db.commit()
    db.refresh(job_desc)
    
    return job_desc


@app.get("/jds/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(jd_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a job description by ID"""
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return jd


@app.post("/variants/compile", response_model=ResumeVariantResponse)
async def compile_variant(
    request: CompileVariantRequest,
    db: Session = Depends(get_db)
):
    """Compile a resume variant for a specific JD and persona"""
    # Validate persona
    valid_personas = ["ic", "architect", "hybrid"]
    if request.persona.lower() not in valid_personas:
        raise HTTPException(
            status_code=400,
            detail=f"Persona must be one of: {', '.join(valid_personas)}"
        )
    
    # Validate platform
    valid_platforms = ["linkedin", "indeed", "dice"]
    if request.platform.lower() not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Platform must be one of: {', '.join(valid_platforms)}"
        )
    
    # Get resume
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get job description
    jd = db.query(JobDescription).filter(JobDescription.id == request.jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Compile variant
    compiled_text = compile_resume_variant(
        resume.raw_text,
        jd.raw_text,
        request.persona.lower(),
        request.platform.lower()
    )
    
    # Calculate scores
    scores = calculate_survivability_score(
        resume.raw_text,
        jd.raw_text,
        request.platform.lower()
    )
    
    # Save variant
    variant = ResumeVariant(
        resume_id=request.resume_id,
        jd_id=request.jd_id,
        persona=request.persona.lower(),
        platform=request.platform.lower(),
        compiled_text=compiled_text,
        scores=scores
    )
    db.add(variant)
    db.commit()
    db.refresh(variant)
    
    return variant


@app.get("/variants/{variant_id}", response_model=ResumeVariantResponse)
async def get_variant(variant_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a resume variant by ID"""
    variant = db.query(ResumeVariant).filter(ResumeVariant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant


@app.get("/variants", response_model=List[ResumeVariantResponse])
async def list_variants(
    resume_id: uuid.UUID = None,
    jd_id: uuid.UUID = None,
    db: Session = Depends(get_db)
):
    """List resume variants with optional filters"""
    query = db.query(ResumeVariant)
    
    if resume_id:
        query = query.filter(ResumeVariant.resume_id == resume_id)
    if jd_id:
        query = query.filter(ResumeVariant.jd_id == jd_id)
    
    variants = query.all()
    return variants


@app.post("/outcomes", response_model=OutcomeResponse)
async def record_outcome(
    outcome: OutcomeCreate,
    db: Session = Depends(get_db)
):
    """Record application outcome (Phase 2)"""
    # Validate status
    valid_statuses = ["rejected", "interview", "ghosted"]
    if outcome.status.lower() not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    # Verify variant exists
    variant = db.query(ResumeVariant).filter(ResumeVariant.id == outcome.variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    # Create outcome
    application_outcome = ApplicationOutcome(
        variant_id=outcome.variant_id,
        status=outcome.status.lower()
    )
    db.add(application_outcome)
    db.commit()
    db.refresh(application_outcome)
    
    return application_outcome


@app.get("/outcomes", response_model=List[OutcomeResponse])
async def list_outcomes(
    variant_id: uuid.UUID = None,
    db: Session = Depends(get_db)
):
    """List application outcomes with optional filter"""
    query = db.query(ApplicationOutcome)
    
    if variant_id:
        query = query.filter(ApplicationOutcome.variant_id == variant_id)
    
    outcomes = query.all()
    return outcomes
