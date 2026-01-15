# Multi-Stage Dockerfile for Stress Detection Application
# Stage 1: Build React frontend
# Stage 2: Build and run Flask backend with static frontend

# ============================================
# STAGE 1: Build React Frontend
# ============================================
FROM node:18-alpine AS frontend-builder

WORKDIR /app/client

# Copy package files
COPY client/package*.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY client/src ./src
COPY client/public ./public

# Build the React application
RUN npm run build

# ============================================
# STAGE 2: Production Image with Flask & Frontend
# ============================================
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .
COPY server/requirements.txt ./server/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn==21.2.0

# Copy ML logic
COPY ml_logic ./ml_logic

# Copy server code
COPY server ./server

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/client/build ./server/static

# Create models directory
RUN mkdir -p ./ml_logic/models ./ml_logic/data

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# Run the Flask application with gunicorn
WORKDIR /app/server

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]
