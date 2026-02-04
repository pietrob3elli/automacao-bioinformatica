"""
Genome Assembly Module
Provides functionality for genome assembly using SPAdes assembler via subprocess.
"""

import subprocess
import os
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GenomeAssembler:
    """
    Wrapper class for genome assembly using SPAdes.
    
    SPAdes (St. Petersburg genome assembler) is a genome assembly algorithm
    designed for single-cell and multi-cell bacterial data.
    """
    
    def __init__(self, forward_reads, reverse_reads, output_dir, 
                 threads=4, careful_mode=False):
        """
        Initialize the GenomeAssembler.
        
        Args:
            forward_reads (str): Path to forward reads FASTQ file
            reverse_reads (str): Path to reverse reads FASTQ file
            output_dir (str): Output directory for assembly results
            threads (int): Number of threads to use (default: 4)
            careful_mode (bool): Run in careful mode to reduce mismatches (default: False)
        """
        self.forward_reads = Path(forward_reads)
        self.reverse_reads = Path(reverse_reads)
        self.output_dir = Path(output_dir)
        self.threads = threads
        self.careful_mode = careful_mode
        
        # Validate inputs
        self._validate_inputs()
    
    def _validate_inputs(self):
        """Validate input files exist."""
        if not self.forward_reads.exists():
            raise FileNotFoundError(f"Forward reads file not found: {self.forward_reads}")
        
        if not self.reverse_reads.exists():
            raise FileNotFoundError(f"Reverse reads file not found: {self.reverse_reads}")
        
        logger.info(f"Input validation passed")
    
    def _check_spades_installed(self):
        """
        Check if SPAdes is installed and available in PATH.
        
        Returns:
            bool: True if SPAdes is installed, False otherwise
        """
        try:
            result = subprocess.run(
                ['spades.py', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"SPAdes version: {result.stdout.strip()}")
                return True
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("SPAdes not found in PATH")
            return False
    
    def run_assembly(self):
        """
        Run SPAdes genome assembly.
        
        Returns:
            bool: True if assembly completed successfully, False otherwise
        """
        # Check if SPAdes is installed
        if not self._check_spades_installed():
            logger.error("SPAdes is not installed or not in PATH")
            logger.info("Please install SPAdes: http://cab.spbu.ru/software/spades/")
            logger.info("For Docker users, this is pre-installed in the container")
            return False
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build SPAdes command
        cmd = [
            'spades.py',
            '-1', str(self.forward_reads),
            '-2', str(self.reverse_reads),
            '-o', str(self.output_dir),
            '-t', str(self.threads)
        ]
        
        if self.careful_mode:
            cmd.append('--careful')
        
        logger.info(f"Running SPAdes assembly...")
        logger.info(f"Command: {' '.join(cmd)}")
        
        try:
            # Run SPAdes
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Stream output
            for line in process.stdout:
                print(line.rstrip())
            
            # Wait for completion
            process.wait()
            
            if process.returncode == 0:
                logger.info("Assembly completed successfully")
                self._log_assembly_results()
                return True
            else:
                stderr_output = process.stderr.read()
                logger.error(f"Assembly failed with return code {process.returncode}")
                logger.error(f"Error output: {stderr_output}")
                return False
                
        except Exception as e:
            logger.error(f"Error running SPAdes: {e}")
            return False
    
    def _log_assembly_results(self):
        """Log information about assembly results."""
        contigs_file = self.output_dir / 'contigs.fasta'
        scaffolds_file = self.output_dir / 'scaffolds.fasta'
        
        if contigs_file.exists():
            logger.info(f"Contigs file: {contigs_file}")
            # Count contigs
            try:
                with open(contigs_file, 'r') as f:
                    contig_count = sum(1 for line in f if line.startswith('>'))
                logger.info(f"Number of contigs: {contig_count}")
            except Exception as e:
                logger.warning(f"Could not count contigs: {e}")
        
        if scaffolds_file.exists():
            logger.info(f"Scaffolds file: {scaffolds_file}")


def main():
    """Example usage of GenomeAssembler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run genome assembly with SPAdes')
    parser.add_argument('-1', '--forward', required=True, help='Forward reads FASTQ')
    parser.add_argument('-2', '--reverse', required=True, help='Reverse reads FASTQ')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads')
    parser.add_argument('--careful', action='store_true', help='Careful mode')
    
    args = parser.parse_args()
    
    assembler = GenomeAssembler(
        forward_reads=args.forward,
        reverse_reads=args.reverse,
        output_dir=args.output,
        threads=args.threads,
        careful_mode=args.careful
    )
    
    success = assembler.run_assembly()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
