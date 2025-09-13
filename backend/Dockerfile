# Use a more secure, slim Bullseye-based Python image
FROM python:3.11.10-slim-bullseye AS base

# Set working directory
WORKDIR /app

# Install system dependencies
# - build-essential: compilation
# - libpq-dev: PostgreSQL client
# - ffmpeg: audio processing
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy setup script & requirements
COPY setup_venv.sh requirements.txt ./

# Make setup script executable
RUN chmod +x setup_venv.sh

# Run setup script to create virtual environment & install dependencies
RUN ./setup_venv.sh

# Copy backend application code
COPY app ./app

# Add virtualenv to PATH
ENV PATH="/app/venv/bin:$PATH"

# Expose FastAPI port
EXPOSE 8000

# Use a non-root user for security
RUN useradd -m appuser
USER appuser

# Command to start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
