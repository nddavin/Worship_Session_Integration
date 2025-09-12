# Use official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy setup script and requirements
COPY setup_venv.sh requirements.txt ./

# Make setup script executable
RUN chmod +x setup_venv.sh

# Run setup script to create venv and install dependencies
RUN ./setup_venv.sh

# Copy backend code
COPY app ./app

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
