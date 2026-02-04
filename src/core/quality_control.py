"""
Quality control module for genomic sequence data.

This module provides functionality to run FastQC and other quality control
tools on sequencing data.
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict
from .command_executor import CommandExecutor


logger = logging.getLogger(__name__)


class QualityControl:
    """
    Perform quality control on sequencing data.
    
    This class provides methods to run FastQC and other QC tools
    on FASTQ files for prokaryotic genome analysis.
    """
    
    def __init__(self, executor: Optional[CommandExecutor] = None):
        """
        Initialize the QualityControl module.
        
        Args:
            executor: Optional CommandExecutor instance. If None, creates a new one.
        """
        self.executor = executor or CommandExecutor()
        logger.info("QualityControl module initialized")
    
    def run_fastqc(
        self,
        input_files: List[Path],
        output_dir: Path,
        threads: int = 1,
        additional_options: Optional[str] = None
    ) -> bool:
        """
        Run FastQC on input FASTQ files.
        
        Args:
            input_files: List of FASTQ file paths to analyze.
            output_dir: Directory to store FastQC output.
            threads: Number of threads to use (default: 1).
            additional_options: Additional FastQC options as a string.
        
        Returns:
            True if FastQC completed successfully, False otherwise.
        
        Raises:
            FileNotFoundError: If input files don't exist.
            RuntimeError: If FastQC is not available.
        
        Example:
            >>> qc = QualityControl()
            >>> files = [Path("sample_R1.fastq"), Path("sample_R2.fastq")]
            >>> qc.run_fastqc(files, Path("qc_output"), threads=4)
        """
        logger.info(f"Running FastQC on {len(input_files)} files")
        
        # Check if FastQC is available
        if not self.executor.check_tool_available("fastqc"):
            raise RuntimeError("FastQC is not available. Please install it first.")
        
        # Check input files exist
        for file in input_files:
            if not file.exists():
                raise FileNotFoundError(f"Input file not found: {file}")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build FastQC command
        file_list = " ".join(str(f) for f in input_files)
        command = f"fastqc {file_list} -o {output_dir} -t {threads}"
        
        if additional_options:
            command += f" {additional_options}"
        
        try:
            code, stdout, stderr = self.executor.run_command(command, timeout=3600)
            logger.info(f"FastQC completed successfully. Output in {output_dir}")
            return True
        except Exception as e:
            logger.error(f"FastQC failed: {str(e)}")
            return False
    
    def check_quality_metrics(self, fastqc_data_file: Path) -> Dict[str, str]:
        """
        Parse FastQC results and extract key quality metrics.
        
        Args:
            fastqc_data_file: Path to fastqc_data.txt file.
        
        Returns:
            Dictionary containing quality metrics.
        
        Example:
            >>> qc = QualityControl()
            >>> metrics = qc.check_quality_metrics(Path("fastqc_data.txt"))
            >>> print(f"Total sequences: {metrics.get('total_sequences')}")
        """
        logger.info(f"Parsing FastQC data from: {fastqc_data_file}")
        
        metrics = {}
        
        if not fastqc_data_file.exists():
            logger.warning(f"FastQC data file not found: {fastqc_data_file}")
            return metrics
        
        try:
            with open(fastqc_data_file, 'r') as f:
                for line in f:
                    if line.startswith("Total Sequences"):
                        metrics['total_sequences'] = line.split('\t')[1].strip()
                    elif line.startswith("Sequences flagged as poor quality"):
                        metrics['poor_quality'] = line.split('\t')[1].strip()
                    elif line.startswith("Sequence length"):
                        metrics['sequence_length'] = line.split('\t')[1].strip()
                    elif line.startswith("%GC"):
                        metrics['gc_content'] = line.split('\t')[1].strip()
            
            logger.info(f"Extracted {len(metrics)} quality metrics")
            return metrics
            
        except Exception as e:
            logger.error(f"Error parsing FastQC data: {str(e)}")
            return metrics
    
    def run_multiqc(
        self,
        input_dir: Path,
        output_dir: Path,
        report_name: str = "multiqc_report"
    ) -> bool:
        """
        Run MultiQC to aggregate FastQC reports.
        
        Args:
            input_dir: Directory containing FastQC outputs.
            output_dir: Directory to store MultiQC report.
            report_name: Name for the MultiQC report (default: multiqc_report).
        
        Returns:
            True if MultiQC completed successfully, False otherwise.
        
        Example:
            >>> qc = QualityControl()
            >>> qc.run_multiqc(Path("qc_results"), Path("reports"))
        """
        logger.info(f"Running MultiQC on: {input_dir}")
        
        # Check if MultiQC is available
        if not self.executor.check_tool_available("multiqc"):
            logger.warning("MultiQC is not available. Skipping aggregation.")
            return False
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build MultiQC command
        command = f"multiqc {input_dir} -o {output_dir} -n {report_name}"
        
        try:
            code, stdout, stderr = self.executor.run_command(command, timeout=600)
            logger.info(f"MultiQC completed successfully. Report in {output_dir}")
            return True
        except Exception as e:
            logger.error(f"MultiQC failed: {str(e)}")
            return False
