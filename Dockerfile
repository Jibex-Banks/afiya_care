FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Create models directory
RUN mkdir -p /app/models && \
    useradd -m -u 1000 user && \
    chown -R user:user /app

USER user

# Set environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s \
    CMD curl -f http://localhost:7860/health || exit 1

# Start server
CMD uvicorn main:app --host 0.0.0.0 --port 7860 --workers 1