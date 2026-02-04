# Example CSV Data for Testing

This directory contains example data files that can be used to test
the file I/O and report generation functionality.

## sample_data.csv

Example quality metrics in CSV format:

```csv
sample_name,total_sequences,gc_content,poor_quality,status
sample_001,1500000,52.3,0,pass
sample_002,1800000,51.7,120,pass
sample_003,1200000,53.1,0,pass
```

## assembly_stats.tsv

Example assembly statistics in TSV format:

```tsv
sample_name	num_contigs	total_length	n50	longest_contig
sample_001	42	4567890	125000	345000
sample_002	38	4321000	138000	412000
sample_003	51	4890000	102000	298000
```

## Usage

You can use the FileHandler class to read these files:

```python
from src.utils.file_io import FileHandler
from pathlib import Path

# Read CSV
handler = FileHandler()
data = handler.read_csv(Path("examples/sample_data.csv"))

for row in data:
    print(f"{row['sample_name']}: {row['total_sequences']} sequences")

# Read TSV
stats = handler.read_csv(Path("examples/assembly_stats.tsv"), delimiter='\t')

for row in stats:
    print(f"{row['sample_name']}: N50 = {row['n50']}")
```

## Creating Reports

Generate a report from this data:

```python
from src.utils.report_generator import ReportGenerator
from pathlib import Path

reporter = ReportGenerator()

# Add a table section from CSV
sections = [
    reporter.add_table_from_csv("Quality Metrics", data),
    reporter.add_table_from_csv("Assembly Statistics", stats)
]

# Create report
reporter.create_report("Example Report", sections, "example_report.md")
```
