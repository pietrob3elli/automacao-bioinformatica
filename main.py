#!/usr/bin/env python3
"""
Bioinformatics Automation Pipeline - Main CLI

This is the main command-line interface for running prokaryotic genome
analysis workflows including quality control, assembly, and reporting.
"""

import argparse
import sys
from pathlib import Path
import logging

from src.core.command_executor import CommandExecutor
from src.core.quality_control import QualityControl
from src.core.assembly import GenomeAssembly
from src.utils.logger import setup_logger
from src.utils.file_io import FileHandler
from src.utils.report_generator import ReportGenerator


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Bioinformatics Automation Pipeline for Prokaryotic Genome Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full QC + Assembly pipeline
  python main.py --workflow full --input data/reads --output results

  # Run only quality control
  python main.py --workflow qc --input data/reads --output qc_results

  # Run only assembly
  python main.py --workflow assembly --input data/reads --output assembly_out

For more information, visit: https://github.com/pietrob3elli/automacao-bioinformatica
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--workflow',
        type=str,
        choices=['qc', 'assembly', 'full'],
        required=True,
        help='Workflow to run: qc (quality control), assembly, or full (QC + assembly)'
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input directory containing FASTQ files or specific FASTQ file'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output directory for results'
    )
    
    # Optional arguments
    parser.add_argument(
        '--forward',
        type=Path,
        help='Forward reads (R1) FASTQ file (for assembly workflow)'
    )
    
    parser.add_argument(
        '--reverse',
        type=Path,
        help='Reverse reads (R2) FASTQ file (for assembly workflow)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=1,
        help='Number of threads to use (default: 1)'
    )
    
    parser.add_argument(
        '--memory',
        type=int,
        default=16,
        help='Memory limit in GB for assembly (default: 16)'
    )
    
    parser.add_argument(
        '--sample-name',
        type=str,
        default='sample',
        help='Sample name for reports (default: sample)'
    )
    
    parser.add_argument(
        '--log-file',
        type=Path,
        help='Path to log file (default: output_dir/pipeline.log)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip report generation'
    )
    
    return parser.parse_args()


def run_quality_control(args, logger):
    """
    Run quality control workflow.
    
    Args:
        args: Parsed command-line arguments.
        logger: Logger instance.
    
    Returns:
        Dictionary with QC results or None if failed.
    """
    logger.info("=" * 60)
    logger.info("Starting Quality Control Workflow")
    logger.info("=" * 60)
    
    qc_output = args.output / "qc"
    qc = QualityControl()
    
    # Find FASTQ files
    input_path = args.input
    if input_path.is_dir():
        fastq_files = list(input_path.glob("*.fastq")) + list(input_path.glob("*.fq"))
        fastq_files += list(input_path.glob("*.fastq.gz")) + list(input_path.glob("*.fq.gz"))
    else:
        fastq_files = [input_path]
    
    if not fastq_files:
        logger.error(f"No FASTQ files found in {input_path}")
        return None
    
    logger.info(f"Found {len(fastq_files)} FASTQ files to process")
    
    # Run FastQC
    success = qc.run_fastqc(
        input_files=fastq_files,
        output_dir=qc_output,
        threads=args.threads
    )
    
    if success:
        logger.info("Quality control completed successfully")
        return {'qc_output': qc_output, 'num_files': len(fastq_files)}
    else:
        logger.error("Quality control failed")
        return None


def run_assembly(args, logger):
    """
    Run genome assembly workflow.
    
    Args:
        args: Parsed command-line arguments.
        logger: Logger instance.
    
    Returns:
        Dictionary with assembly results or None if failed.
    """
    logger.info("=" * 60)
    logger.info("Starting Genome Assembly Workflow")
    logger.info("=" * 60)
    
    assembly_output = args.output / "assembly"
    assembler = GenomeAssembly()
    
    # Get input files
    forward_reads = args.forward if args.forward else args.input
    reverse_reads = args.reverse
    
    if not forward_reads or not forward_reads.exists():
        logger.error(f"Forward reads file not found: {forward_reads}")
        return None
    
    logger.info(f"Forward reads: {forward_reads}")
    if reverse_reads:
        logger.info(f"Reverse reads: {reverse_reads}")
    
    # Run SPAdes
    success = assembler.run_spades(
        forward_reads=forward_reads,
        reverse_reads=reverse_reads,
        output_dir=assembly_output,
        threads=args.threads,
        memory=args.memory,
        mode='isolate'
    )
    
    if not success:
        logger.error("Assembly failed")
        return None
    
    # Get assembly statistics
    contigs_file = assembly_output / "contigs.fasta"
    if contigs_file.exists():
        stats = assembler.get_assembly_stats(contigs_file)
        logger.info("Assembly statistics calculated successfully")
        return {
            'assembly_output': assembly_output,
            'contigs_file': contigs_file,
            'stats': stats
        }
    else:
        logger.warning("Contigs file not found")
        return {'assembly_output': assembly_output}


def generate_report(args, logger, qc_results=None, assembly_results=None):
    """
    Generate analysis report.
    
    Args:
        args: Parsed command-line arguments.
        logger: Logger instance.
        qc_results: Quality control results dictionary.
        assembly_results: Assembly results dictionary.
    """
    if args.no_report:
        logger.info("Report generation skipped (--no-report flag)")
        return
    
    logger.info("=" * 60)
    logger.info("Generating Analysis Report")
    logger.info("=" * 60)
    
    reporter = ReportGenerator(output_dir=args.output / "reports")
    sections = []
    
    # Add summary section
    total_samples = 1
    successful = 0
    failed = 0
    
    if qc_results:
        successful += 1
    else:
        failed += 1
    
    if assembly_results:
        successful += 1
    else:
        failed += 1
    
    sections.append(
        reporter.add_summary_section(
            total_samples=total_samples,
            successful=successful,
            failed=failed,
            notes=f"Sample: {args.sample_name}"
        )
    )
    
    # Add QC section if available
    if qc_results:
        qc_metrics = {
            'QC Output Directory': str(qc_results['qc_output']),
            'Number of Files Processed': str(qc_results['num_files']),
            'Status': 'Completed'
        }
        sections.append(
            reporter.add_qc_section(args.sample_name, qc_metrics)
        )
    
    # Add assembly section if available
    if assembly_results and 'stats' in assembly_results:
        sections.append(
            reporter.add_assembly_section(args.sample_name, assembly_results['stats'])
        )
    
    # Create report
    report_path = reporter.create_report(
        title=f"Bioinformatics Analysis Report - {args.sample_name}",
        sections=sections,
        output_file=f"{args.sample_name}_report.md"
    )
    
    logger.info(f"Report generated: {report_path}")


def main():
    """
    Main entry point for the pipeline.
    """
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    log_level = getattr(logging, args.log_level)
    log_file = args.log_file or (args.output / "pipeline.log")
    logger = setup_logger(
        name="bioinformatics_pipeline",
        level=log_level,
        log_file=log_file,
        console=True
    )
    
    logger.info("=" * 60)
    logger.info("Bioinformatics Automation Pipeline")
    logger.info("=" * 60)
    logger.info(f"Workflow: {args.workflow}")
    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")
    logger.info(f"Threads: {args.threads}")
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    qc_results = None
    assembly_results = None
    
    try:
        # Run selected workflow
        if args.workflow in ['qc', 'full']:
            qc_results = run_quality_control(args, logger)
            if not qc_results and args.workflow == 'qc':
                logger.error("QC workflow failed")
                return 1
        
        if args.workflow in ['assembly', 'full']:
            assembly_results = run_assembly(args, logger)
            if not assembly_results and args.workflow == 'assembly':
                logger.error("Assembly workflow failed")
                return 1
        
        # Generate report
        generate_report(args, logger, qc_results, assembly_results)
        
        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
