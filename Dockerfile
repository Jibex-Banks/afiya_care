# Use a recent CUDA version (12.x recommended for latest torch/bitsandbytes)
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04  # Or 12.6 if available; runtime for inference (smaller than devel)

# Install Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3.11-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

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