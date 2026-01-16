# ATS Resume Compiler - Frontend

Next.js frontend for the ATS Resume Compiler application.

## Prerequisites

- Node.js 18+ 
- npm or yarn

## Local Development

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local and set NEXT_PUBLIC_API_URL if backend is not on localhost:8000
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   - http://localhost:3000

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: `http://localhost:8000`)

## Build for Production

```bash
npm run build
npm start
```

## Lovable.dev Deployment

See [../LOVABLE_SETUP.md](../LOVABLE_SETUP.md) for deployment instructions.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css         # Global styles
├── components/            # React components
│   ├── ResumeUpload.tsx
│   ├── JobDescriptionInput.tsx
│   └── VariantComparison.tsx
├── lib/                   # Utilities
│   └── api.ts             # API client
└── package.json
```
