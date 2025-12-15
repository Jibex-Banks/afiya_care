# Optimized for Hugging Face Spaces
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages with cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Create non-root user
RUN useradd -m -u 1000 user && \
    mkdir -p /app/models && \
    chown -R user:user /app

USER user

# Hugging Face Spaces needs port 7860
ENV PORT=7860
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s \
    CMD curl -f http://localhost:7860/health || exit 1

# Start server
CMD uvicorn main:app --host 0.0.0.0 --port 7860 --workers 1