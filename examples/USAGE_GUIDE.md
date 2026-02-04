# Example Usage Guide

## Basic Examples

### 1. Quality Control on a Single Sample

```bash
# Using local installation
python main.py \
  --workflow qc \
  --input data/sample_R1.fastq \
  --output results/qc_sample \
  --sample-name sample_001 \
  --threads 4

# Using Docker
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow qc \
  --input /data/sample_R1.fastq \
  --output /results/qc_sample \
  --sample-name sample_001 \
  --threads 4
```

### 2. Genome Assembly

```bash
# Using local installation
python main.py \
  --workflow assembly \
  --forward data/sample_R1.fastq.gz \
  --reverse data/sample_R2.fastq.gz \
  --output results/assembly \
  --sample-name sample_001 \
  --threads 8 \
  --memory 32

# Using Docker
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow assembly \
  --forward /data/sample_R1.fastq.gz \
  --reverse /data/sample_R2.fastq.gz \
  --output /results/assembly \
  --sample-name sample_001 \
  --threads 8 \
  --memory 32
```

### 3. Full Pipeline (QC + Assembly)

```bash
# Using local installation
python main.py \
  --workflow full \
  --input data/reads/ \
  --output results/full_analysis \
  --sample-name sample_001 \
  --threads 8 \
  --memory 32 \
  --log-level DEBUG

# Using Docker
docker run -v $(pwd)/data:/data -v $(pwd)/results:/results \
  bioinformatics-pipeline:latest \
  --workflow full \
  --input /data/reads/ \
  --output /results/full_analysis \
  --sample-name sample_001 \
  --threads 8 \
  --memory 32 \
  --log-level DEBUG
```

## Advanced Examples

### Batch Processing Multiple Samples

```bash
#!/bin/bash
# Process multiple samples in a loop

SAMPLES=("sample_001" "sample_002" "sample_003")

for SAMPLE in "${SAMPLES[@]}"; do
  echo "Processing $SAMPLE..."
  
  python main.py \
    --workflow full \
    --forward data/${SAMPLE}_R1.fastq.gz \
    --reverse data/${SAMPLE}_R2.fastq.gz \
    --output results/${SAMPLE} \
    --sample-name $SAMPLE \
    --threads 8 \
    --memory 32
  
  echo "$SAMPLE completed!"
done
```

### Using Custom Log File

```bash
python main.py \
  --workflow full \
  --input data/reads/ \
  --output results/ \
  --sample-name sample_001 \
  --log-file logs/sample_001.log \
  --log-level INFO
```

### Skip Report Generation

```bash
python main.py \
  --workflow assembly \
  --forward data/sample_R1.fastq.gz \
  --reverse data/sample_R2.fastq.gz \
  --output results/ \
  --sample-name sample_001 \
  --no-report
```

## Expected Input Data

### FASTQ Files

The pipeline accepts:
- Uncompressed FASTQ files (`.fastq`, `.fq`)
- Gzip-compressed FASTQ files (`.fastq.gz`, `.fq.gz`)
- Single-end or paired-end reads

### Directory Structure

For best results, organize your data as follows:

```
data/
├── sample_001_R1.fastq.gz  # Forward reads
├── sample_001_R2.fastq.gz  # Reverse reads
├── sample_002_R1.fastq.gz
├── sample_002_R2.fastq.gz
└── ...
```

## Output Files

After running the pipeline, you'll find:

### Quality Control Output
- `qc/sample_fastqc.html` - HTML quality report
- `qc/sample_fastqc.zip` - Detailed QC data

### Assembly Output
- `assembly/contigs.fasta` - Assembled contigs
- `assembly/scaffolds.fasta` - Assembled scaffolds
- `assembly/spades.log` - Assembly log

### Reports
- `reports/sample_report.md` - Markdown summary
- `pipeline.log` - Execution log

## Troubleshooting

### Common Issues

1. **Tool not found**: Make sure bioinformatics tools are installed and in PATH
2. **Out of memory**: Increase `--memory` parameter
3. **Timeout errors**: Increase timeout in code or use more threads
4. **Permission errors with Docker**: Use `sudo` or add user to docker group

### Getting Help

```bash
python main.py --help
```

Or run Docker container without arguments:

```bash
docker run bioinformatics-pipeline:latest
```
