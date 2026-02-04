# Bioinformatics Automation Pipeline Dockerfile
# 
# This Dockerfile creates a containerized environment for prokaryotic genome
# analysis with all necessary bioinformatics tools pre-installed.
#
# Build: docker build -t bioinformatics-pipeline:latest .
# Run: docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
#      bioinformatics-pipeline:latest --workflow full --input /data --output /results

FROM ubuntu:22.04

# Set metadata
LABEL maintainer="Pietro B3elli"
LABEL description="Bioinformatics automation pipeline for prokaryotic genome analysis"
LABEL version="1.0.0"

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies and bioinformatics tools
RUN apt-get update && apt-get install -y \
    # System utilities
    wget \
    curl \
    git \
    unzip \
    default-jre \
    # Python and development tools
    python3 \
    python3-pip \
    python3-dev \
    # Build essentials for compiling tools
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    # Bioinformatics tools
    fastqc \
    && rm -rf /var/lib/apt/lists/*

# Install SPAdes genome assembler
RUN wget https://github.com/ablab/spades/releases/download/v3.15.5/SPAdes-3.15.5-Linux.tar.gz && \
    tar -xzf SPAdes-3.15.5-Linux.tar.gz && \
    mv SPAdes-3.15.5-Linux /opt/spades && \
    ln -s /opt/spades/bin/spades.py /usr/local/bin/spades.py && \
    ln -s /opt/spades/bin/metaspades.py /usr/local/bin/metaspades.py && \
    rm SPAdes-3.15.5-Linux.tar.gz

# Install QUAST for assembly quality assessment
RUN wget https://github.com/ablab/quast/releases/download/quast_5.2.0/quast-5.2.0.tar.gz && \
    tar -xzf quast-5.2.0.tar.gz && \
    cd quast-5.2.0 && \
    python3 setup.py install && \
    cd .. && \
    rm quast-5.2.0.tar.gz

# Install MultiQC for aggregating QC reports
RUN pip3 install --no-cache-dir multiqc

# Copy application code
COPY src/ /app/src/
COPY main.py /app/
COPY requirements.txt /app/

# Install Python dependencies (if any additional are needed)
RUN pip3 install --no-cache-dir -r requirements.txt

# Create directories for data
RUN mkdir -p /data /results

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Make main.py executable
RUN chmod +x /app/main.py

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ "$#" -eq 0 ]; then\n\
    echo "Bioinformatics Automation Pipeline"\n\
    echo "==================================="\n\
    echo ""\n\
    echo "Usage: docker run -v \$(pwd)/data:/data -v \$(pwd)/results:/results \\"\n\
    echo "       bioinformatics-pipeline:latest [OPTIONS]"\n\
    echo ""\n\
    echo "Examples:"\n\
    echo "  # Run full pipeline"\n\
    echo "  docker run -v \$(pwd)/data:/data -v \$(pwd)/results:/results \\"\n\
    echo "    bioinformatics-pipeline:latest --workflow full --input /data --output /results"\n\
    echo ""\n\
    echo "  # Run only quality control"\n\
    echo "  docker run -v \$(pwd)/data:/data -v \$(pwd)/results:/results \\"\n\
    echo "    bioinformatics-pipeline:latest --workflow qc --input /data --output /results"\n\
    echo ""\n\
    python3 /app/main.py --help\n\
else\n\
    python3 /app/main.py "$@"\n\
fi' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command (shows help)
CMD []

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Volume mount points
VOLUME ["/data", "/results"]
