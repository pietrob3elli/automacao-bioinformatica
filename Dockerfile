# Bioinformatics Automation Pipeline Dockerfile
# Baseado em Ubuntu para suporte total a ferramentas de Bioinformática
FROM ubuntu:22.04

# Metadados e Labels
LABEL maintainer="Jhenifer"
LABEL description="Bioinformatics automation pipeline for prokaryotic genome analysis"
LABEL version="1.0.0"

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho
WORKDIR /app

# 1. Instalação de dependências do sistema e ferramentas de Bioinfo
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    unzip \
    default-jre \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    fastqc \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalação do SPAdes (Assembler para Procariotos - Requisito da Vaga)
RUN wget https://github.com/ablab/spades/releases/download/v3.15.5/SPAdes-3.15.5-Linux.tar.gz && \
    tar -xzf SPAdes-3.15.5-Linux.tar.gz && \
    mv SPAdes-3.15.5-Linux /opt/spades && \
    ln -s /opt/spades/bin/spades.py /usr/local/bin/spades.py && \
    rm SPAdes-3.15.5-Linux.tar.gz

# 3. Instalação do QUAST (Avaliação de Qualidade)
RUN pip3 install --no-cache-dir multiqc

# 4. Configuração do Código e Dependências Python
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY main.py /app/

# Configurações de ambiente
ENV PYTHONPATH=/app:$PYTHONPATH
RUN mkdir -p /data /results
RUN chmod +x /app/main.py

# Entrypoint para facilitar o uso no terminal/VMs
RUN echo '#!/bin/bash\n\
if [ "$#" -eq 0 ]; then\n\
    python3 /app/main.py --help\n\
else\n\
    python3 /app/main.py "$@"\n\
fi' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
VOLUME ["/data", "/results"]