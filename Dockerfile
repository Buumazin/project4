# Multi-stage Dockerfile for FinAlly (Fullstack)

# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend .
RUN npm run build

# Stage 2: Backend app
FROM python:3.12-slim
WORKDIR /app

# Install backend dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend/src ./backend/src
COPY backend/pyproject.toml ./backend/pyproject.toml

# Copy static frontend build (optional for static serving)
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public

# Ensure DB folder exists
RUN mkdir -p /app/db

# Expose port
EXPOSE 8000

# Runtime environment variables
ENV DATABASE_URL sqlite:///./db/finally.db

# Start the backend service
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
