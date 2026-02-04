# Bioinformatics Automation: Prokaryotic Genome Pipeline 🧬🤖

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

**Modular Python pipeline for prokaryotic genome and metagenome processing, focusing on report automation and Docker-based reproducibility.**

This repository demonstrates a full-stack bioinformatics approach, translating raw sequencing data (FASTQ) into structured insights, tailored for high-performance remote Linux environments (VMs via SSH/SCP).

---

## 📋 Features

- **Modular Architecture**: Clean separation of concerns between assembly logic (`src/genome_assembly.py`) and analytics (`src/data_visualization.py`).
- **Genome Assembly**: Automated SPAdes integration for *de novo* prokaryotic assembly.
- **Data Visualization**: Dynamic generation of assembly metrics (N50, GC content) using Pandas and Matplotlib.
- **Interactive Dashboard**: Modern Next.js web dashboard for visualizing pipeline results with Recharts and Tailwind CSS. See [dashboard/README.md](dashboard/README.md) for details.
- **Automated Reporting**: Scripted conversion of technical CSV/TSV outputs into readable Markdown summaries.
- **Containerization**: Full Dockerfile support to ensure consistent environments across different servers.
- **Professional Logging**: Implementation of the `logging` module for audit trails in automated processes.

## 🏗️ Project Structure

```text
automacao-bioinformatica/
├── src/
│   ├── __init__.py
│   ├── genome_assembly.py    # Subprocess-based assembly orchestration
│   └── data_visualization.py # Pandas-based data analytics and plotting
├── data/                     # Input directory (FASTQ/CSV samples)
├── dashboard/                # Next.js web dashboard for visualizing results
├── main.py                   # CLI entry point with argparse
├── requirements.txt          # Python dependency manifest
├── Dockerfile                # Environment recipe (Ubuntu 22.04 + Bio tools)
└── README.md                 # Technical documentation
