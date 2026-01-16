# ATS-Aware Resume Compiler

A resume survivability + translation system designed to help resumes pass ATS and AI screening.

## Overview

This is **not** a resume builder. It is a **resume survivability + translation system** designed to help resumes pass ATS and AI screening by translating a single source-of-truth resume into ATS-optimized variants per:
- Job description
- Platform (LinkedIn / Indeed / Dice)
- Persona (IC / Architect / Hybrid)

## Architecture

```
Frontend (Web App)
 ├── Resume Upload
 ├── Job Description Input
 ├── Variant Comparison
 └── Export & Tracking

Backend (API)
 ├── Resume Parser
 ├── JD Intelligence Engine
 ├── Platform Heuristics
 ├── Resume Compiler
 ├── Survivability Scoring
 └── Outcome Feedback

Data Layer
 ├── PostgreSQL (truth + variants)
 ├── Redis (queue/cache)
 └── Object Storage (resume files – later)
```

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

### Frontend (Coming Soon)
- Next.js (App Router)
- TypeScript
- TailwindCSS + shadcn/ui

## Quick Start

See [START_HERE.md](./START_HERE.md) for detailed setup instructions.

### Quick Start (Docker)

1. **Set up environment:**
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Start backend services:**
   ```bash
   docker compose up --build
   ```

3. **Start frontend (separate terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

### Resume Management
- `POST /resumes/upload` - Upload and parse a resume
- `GET /resumes/{resume_id}` - Get a resume by ID
- `GET /resumes` - List all resumes for a user

### Job Descriptions
- `POST /jds` - Create a job description and extract signals
- `GET /jds/{jd_id}` - Get a job description by ID

### Resume Variants
- `POST /variants/compile` - Compile a resume variant
- `GET /variants/{variant_id}` - Get a variant by ID
- `GET /variants` - List variants with optional filters

### Outcomes (Phase 2)
- `POST /outcomes` - Record application outcome
- `GET /outcomes` - List outcomes with optional filter

## Core Features

### Resume Parsing
- Supports PDF, DOCX, and TXT formats
- Extracts plain text while preserving truth
- Ignores formatting (MVP)

### Job Description Intelligence
- Extracts top keyword clusters
- Detects seniority indicators
- Identifies hands-on bias
- Flags fast-paced/junior bias

### Resume Compiler
- Never invents skills
- Only reuses content already present
- Emphasizes JD-matching terms only if found in resume
- Creates persona-based summaries

### Survivability Scoring
- Keyword Match Score
- Title Alignment Score
- Age Proxy Risk
- Overqualification Risk
- Platform Confidence

## Legal & Compliance

- User-initiated actions only
- No scraping credentials
- No automated job submissions
- No falsification of experience
- Clear disclaimers

## Development Roadmap

### Week 1 ✅
- [x] DB schema
- [x] Resume parser
- [x] JD extraction
- [x] Basic API

### Week 2 ✅
- [x] Compiler logic
- [x] Platform profiles
- [x] Survivability scoring

### Week 3 (In Progress)
- [ ] Variant comparison
- [ ] Export (text first)
- [ ] Outcome logging

### Week 4 (Planned)
- [ ] UI polish
- [ ] Stripe (optional)
- [ ] Private beta

## Planned Upgrades (After MVP)

1. LLM-backed compiler with evidence citations
2. DOCX/PDF export templates
3. Outcome-driven learning loop
4. Read-only browser extension
5. Enterprise / outplacement SKU

## License

[To be determined]
"# ATS-Filter" 
