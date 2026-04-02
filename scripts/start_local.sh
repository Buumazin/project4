#!/usr/bin/env bash
set -e

# Copy environment
cp .env.example .env

# Build frontend
cd frontend
npm ci
npm run build
cd ..

# Start backend
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
