# Bioinformatics Automation: Prokaryotic Genome Pipeline 🧬🤖

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/next.js-000000?style=flat&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Docker Support](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Modular Python pipeline for prokaryotic genome and metagenome processing, featuring report automation, Docker-based reproducibility, and an interactive Next.js dashboard.**

This repository demonstrates a full-stack bioinformatics approach, translating raw sequencing data (FASTQ) into structured insights, tailored for high-performance remote Linux environments (VMs via SSH/SCP).

---

## 📋 Features

- **Modular Architecture**: Clean separation of concerns between assembly logic (`src/genome_assembly.py`) and analytics (`src/data_visualization.py`).
- **Genome Assembly**: Automated SPAdes integration for *de novo* prokaryotic assembly, including threads and memory optimization.
- **Interactive Dashboard**: Modern **Next.js** web interface built with **Recharts** and **Tailwind CSS** for dynamic visualization of results.
- **Data Insights**: Automated calculation and plotting of key metrics: **N50**, **GC Content**, and **Contig Distribution**.
- **Containerization**: Full **Dockerfile** support to ensure consistent environments and easy deployment on remote servers.
- **Professional Logging**: Implementation of the `logging` module for robust audit trails in automated production pipelines.

## 🏗️ Project Structure

```text
automacao-bioinformatica/
├── src/
│   ├── __init__.py
│   ├── genome_assembly.py    # Subprocess-based assembly orchestration
│   └── data_visualization.py # Pandas-based data analytics and plotting
├── data/                     # Input directory (FASTQ/CSV samples)
├── dashboard/                # Next.js web dashboard for results visualization
├── main.py                   # CLI entry point with argparse (subcommands)
├── requirements.txt          # Python dependency manifest
├── Dockerfile                # Environment recipe (Ubuntu 22.04 + Bio tools)
└── README.md                 # Technical documentation
