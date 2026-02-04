# Automação Bioinformática

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Pipeline modular em Python para processamento de genomas procariontes e metagenomas, com foco em automação de laudos e reprodutibilidade via Docker.

A professional bioinformatics automation pipeline for prokaryotic genome analysis, featuring quality control, assembly, and automated reporting.

## 📋 Features

- **Modular Architecture**: Clean separation of concerns with `src/core/` for processing logic and `src/utils/` for helpers
- **Quality Control**: FastQC and MultiQC integration for sequencing data QC
- **Genome Assembly**: SPAdes integration for de novo prokaryotic genome assembly
- **Automated Reporting**: Generate professional Markdown reports from analysis results
- **Command Execution**: Safe subprocess management for running bioinformatics tools
- **Docker Support**: Fully containerized environment for reproducibility
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Professional Documentation**: Extensive docstrings and type hints

## 🏗️ Project Structure

```
automacao-bioinformatica/
├── src/
│   ├── __init__.py
│   ├── core/                    # Core processing logic
│   │   ├── __init__.py
│   │   ├── command_executor.py  # Shell command execution
│   │   ├── quality_control.py   # FastQC/MultiQC wrapper
│   │   └── assembly.py          # SPAdes/QUAST wrapper
│   └── utils/                   # Helper utilities
│       ├── __init__.py
│       ├── logger.py            # Logging configuration
│       ├── file_io.py           # File I/O for CSV/TSV/FASTA
│       └── report_generator.py  # Markdown report generation
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── README.md                    # This file
└── LICENSE                      # MIT License

```

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Build the Docker image:**

```bash
docker build -t bioinformatics-pipeline:latest .
```

2. **Run the pipeline:**

```bash
# Full pipeline (QC + Assembly)
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow full \
  --input /data \
  --output /results \
  --sample-name my_sample \
  --threads 4

# Quality control only
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow qc \
  --input /data \
  --output /results \
  --threads 4

# Assembly only
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow assembly \
  --forward /data/sample_R1.fastq \
  --reverse /data/sample_R2.fastq \
  --output /results \
  --threads 4
```

### Option 2: Local Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Install bioinformatics tools:**

- FastQC: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- SPAdes: https://github.com/ablab/spades
- MultiQC (optional): `pip install multiqc`
- QUAST (optional): https://github.com/ablab/quast

3. **Run the pipeline:**

```bash
python main.py --workflow full --input data/ --output results/ --threads 4
```

## 📖 Usage

### Command Line Interface

```bash
python main.py [OPTIONS]

Required Arguments:
  --workflow {qc,assembly,full}  Workflow to run
  --input PATH                   Input directory or FASTQ file
  --output PATH                  Output directory

Optional Arguments:
  --forward PATH                 Forward reads (R1) FASTQ file
  --reverse PATH                 Reverse reads (R2) FASTQ file
  --threads INT                  Number of threads (default: 1)
  --memory INT                   Memory limit in GB (default: 16)
  --sample-name STR              Sample name for reports (default: sample)
  --log-file PATH                Path to log file
  --log-level {DEBUG,INFO,WARNING,ERROR}  Logging level (default: INFO)
  --no-report                    Skip report generation
  --help                         Show help message
```

### Examples

**Run full pipeline on paired-end reads:**

```bash
python main.py \
  --workflow full \
  --input data/reads/ \
  --output results/ \
  --sample-name sample_001 \
  --threads 8 \
  --memory 32
```

**Run quality control on multiple FASTQ files:**

```bash
python main.py \
  --workflow qc \
  --input data/fastq_files/ \
  --output qc_results/ \
  --threads 4
```

**Run assembly with specific forward/reverse reads:**

```bash
python main.py \
  --workflow assembly \
  --forward data/sample_R1.fastq.gz \
  --reverse data/sample_R2.fastq.gz \
  --output assembly_results/ \
  --threads 8 \
  --memory 32
```

## 🔬 Workflow Details

### Quality Control Workflow

1. Runs FastQC on all FASTQ files
2. Generates quality reports with per-base quality, GC content, etc.
3. Optionally aggregates results with MultiQC
4. Creates summary report

### Assembly Workflow

1. Runs SPAdes genome assembler on reads
2. Calculates assembly statistics (N50, total length, number of contigs)
3. Optionally runs QUAST for quality assessment
4. Creates assembly report

### Full Workflow

Combines QC and Assembly workflows in sequence.

## 📊 Output Structure

```
results/
├── qc/                          # Quality control outputs
│   ├── sample_R1_fastqc.html
│   ├── sample_R1_fastqc.zip
│   └── ...
├── assembly/                    # Assembly outputs
│   ├── contigs.fasta           # Assembled contigs
│   ├── scaffolds.fasta         # Assembled scaffolds
│   ├── spades.log
│   └── ...
├── reports/                     # Generated reports
│   └── sample_report.md        # Markdown summary report
└── pipeline.log                 # Execution log
```

## 🧪 Code Quality

This pipeline demonstrates professional software engineering practices:

- **Comprehensive Docstrings**: Every function and class is documented
- **Type Hints**: Enhanced code clarity and IDE support
- **Error Handling**: Robust exception handling throughout
- **Logging**: Detailed logging for debugging and monitoring
- **Modular Design**: Separation of concerns and reusable components
- **Security**: Safe subprocess execution with proper sanitization

## 🐳 Docker Details

The Dockerfile includes:
- Ubuntu 22.04 base image
- Python 3 with pip
- FastQC, SPAdes, QUAST, and MultiQC pre-installed
- Optimized for reproducibility
- Volume mounts for data and results
- Health checks for container monitoring

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Pietro B3elli

## 🙏 Acknowledgments

- FastQC: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- SPAdes: https://github.com/ablab/spades
- MultiQC: https://multiqc.info/
- QUAST: https://github.com/ablab/quast

## 📚 Citation

If you use this pipeline in your research, please cite:

```
B3elli, P. (2026). Bioinformatics Automation Pipeline for Prokaryotic Genome Analysis.
GitHub repository: https://github.com/pietrob3elli/automacao-bioinformatica
```
