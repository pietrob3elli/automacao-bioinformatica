# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

# Note: SPAdes installation is commented out due to network restrictions
# In production, you can uncomment and install SPAdes, or use a pre-built image with SPAdes
# Alternatively, install SPAdes manually after building the container
#
# Install SPAdes genome assembler (uncomment when network allows):
# RUN wget http://cab.spbu.ru/files/release3.15.5/SPAdes-3.15.5-Linux.tar.gz && \
#     tar -xzf SPAdes-3.15.5-Linux.tar.gz && \
#     mv SPAdes-3.15.5-Linux /opt/spades && \
#     rm SPAdes-3.15.5-Linux.tar.gz && \
#     ln -s /opt/spades/bin/spades.py /usr/local/bin/spades.py

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY src/ ./src/

# Create directories for data
RUN mkdir -p /app/data /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default command shows help
CMD ["python", "main.py", "--help"]
