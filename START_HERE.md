# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- (Optional) Python 3.11+ for local backend development
- (Optional) Node.js 18+ for local frontend development

## Option 1: Full Docker Setup (Recommended)

### Step 1: Set up environment variables

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY if you have one (optional for MVP)
```

### Step 2: Start all services

```bash
docker compose up --build
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379
- FastAPI backend on port 8000
- (Frontend runs separately - see below)

### Step 3: Start the frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Step 4: Access the application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Option 2: Local Development (Backend Only)

### Step 1: Start database services

```bash
docker compose up postgres redis
```

### Step 2: Set up Python environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 4: Run the backend

```bash
uvicorn app.main:app --reload
```

## Testing the API

### 1. Upload a Resume

```bash
curl -X POST "http://localhost:8000/resumes/upload" \
  -F "file=@/path/to/your/resume.pdf" \
  -F "user_id=test_user"
```

### 2. Create a Job Description

```bash
curl -X POST "http://localhost:8000/jds" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "linkedin",
    "raw_text": "Senior Software Engineer... (paste JD here)"
  }'
```

### 3. Compile a Variant

```bash
curl -X POST "http://localhost:8000/variants/compile" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "YOUR_RESUME_ID",
    "jd_id": "YOUR_JD_ID",
    "persona": "ic",
    "platform": "linkedin"
  }'
```

## Project Structure

```
ATS-Project/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── parsing.py        # Resume parser
│   │   ├── jd_extract.py     # JD intelligence
│   │   ├── compiler.py       # Resume compiler
│   │   └── scoring.py        # Survivability scoring
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   ├── lib/                  # API client
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running: `docker compose ps`
- Check DATABASE_URL in backend/.env

### Port conflicts
- Change ports in docker-compose.yml if 5432, 6379, or 8000 are in use

### Frontend can't connect to backend
- Check NEXT_PUBLIC_API_URL in frontend/.env.local
- Ensure backend is running on port 8000
- Check CORS settings in backend/app/main.py

## Next Steps

1. Upload your resume through the web UI
2. Paste a job description
3. Compile variants for different personas/platforms
4. Review survivability scores
5. Download optimized resume variants

## Development Notes

- Database tables are created automatically on first run
- No migrations needed for MVP (using SQLAlchemy create_all)
- Redis is configured but not actively used in MVP (ready for queue/cache)
- OpenAI API key is optional - MVP works without it
