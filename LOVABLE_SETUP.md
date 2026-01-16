# Lovable.dev Setup Guide

## ✅ Frontend Compatibility

The Next.js frontend is **fully compatible** with Lovable.dev and will run without issues.

## ⚠️ Backend Configuration Required

The frontend expects a backend API. You have two options:

### Option 1: External Backend (Recommended)

1. **Deploy the FastAPI backend separately** (e.g., Railway, Render, Fly.io, or any Python hosting)

2. **Set environment variable in Lovable.dev:**
   - Go to your Lovable.dev project settings
   - Add environment variable: `NEXT_PUBLIC_API_URL`
   - Set value to your backend URL (e.g., `https://your-backend.railway.app`)

3. **The frontend will automatically connect to your backend**

### Option 2: Use Lovable.dev API Routes (Future)

If you want everything in one place, you can create Next.js API routes that proxy to your backend or replicate the backend logic. This requires additional setup.

## Quick Checklist

- ✅ Next.js 14 with App Router
- ✅ TypeScript configured
- ✅ TailwindCSS configured
- ✅ All components use 'use client' directive
- ✅ Environment variable support (`NEXT_PUBLIC_API_URL`)
- ⚠️ Backend must be hosted separately or configured

## Testing Locally Before Deploying

1. **Start backend:**
   ```bash
   docker compose up --build
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Verify connection:**
   - Frontend should connect to `http://localhost:8000` by default
   - Or set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`

## Deployment Steps

1. **Deploy backend first** (Railway, Render, etc.)
2. **Get backend URL** (e.g., `https://ats-backend.railway.app`)
3. **In Lovable.dev:**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Deploy frontend

## Current Status

- ✅ Frontend: Ready for Lovable.dev
- ⚠️ Backend: Needs separate hosting
- ✅ Configuration: Environment variable support ready

The frontend will run successfully in Lovable.dev, but API calls will fail until the backend is configured.
