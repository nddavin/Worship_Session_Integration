FROM python:3.11-slim

WORKDIR /worker

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy setup script and requirements
COPY ../setup_venv.sh ../requirements.txt ./

RUN chmod +x setup_venv.sh
RUN ./setup_venv.sh

# Copy worker code
COPY . .

ENV PATH="/worker/venv/bin:$PATH"

# Start Celery worker
CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
