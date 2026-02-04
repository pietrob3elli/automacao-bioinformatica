"""
Genome assembly module for prokaryotic genomes.

This module provides functionality to run genome assembly tools like SPAdes
on sequencing data.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict
from .command_executor import CommandExecutor


logger = logging.getLogger(__name__)


class GenomeAssembly:
    """
    Perform genome assembly on prokaryotic sequencing data.
    
    This class provides methods to run SPAdes and other assembly tools
    on FASTQ files for prokaryotic genome analysis.
    """
    
    def __init__(self, executor: Optional[CommandExecutor] = None):
        """
        Initialize the GenomeAssembly module.
        
        Args:
            executor: Optional CommandExecutor instance. If None, creates a new one.
        """
        self.executor = executor or CommandExecutor()
        logger.info("GenomeAssembly module initialized")
    
    def run_spades(
        self,
        forward_reads: Path,
        reverse_reads: Optional[Path] = None,
        output_dir: Path = Path("spades_output"),
        threads: int = 1,
        memory: int = 16,
        mode: str = "isolate"
    ) -> bool:
        """
        Run SPAdes genome assembler on paired-end or single-end reads.
        
        Args:
            forward_reads: Path to forward reads (R1) FASTQ file.
            reverse_reads: Optional path to reverse reads (R2) FASTQ file.
            output_dir: Directory to store assembly output.
            threads: Number of threads to use (default: 1).
            memory: Memory limit in GB (default: 16).
            mode: Assembly mode - 'isolate', 'meta', or 'rna' (default: 'isolate').
        
        Returns:
            True if assembly completed successfully, False otherwise.
        
        Raises:
            FileNotFoundError: If input files don't exist.
            RuntimeError: If SPAdes is not available.
        
        Example:
            >>> assembler = GenomeAssembly()
            >>> assembler.run_spades(
            ...     Path("sample_R1.fastq"),
            ...     Path("sample_R2.fastq"),
            ...     Path("assembly_out"),
            ...     threads=8
            ... )
        """
        logger.info(f"Starting SPAdes assembly in {mode} mode")
        
        # Check if SPAdes is available
        spades_cmd = "spades.py" if mode == "isolate" else f"{mode}spades.py"
        if not self.executor.check_tool_available(spades_cmd):
            raise RuntimeError(f"SPAdes ({spades_cmd}) is not available. Please install it first.")
        
        # Check input files exist
        if not forward_reads.exists():
            raise FileNotFoundError(f"Forward reads file not found: {forward_reads}")
        
        if reverse_reads and not reverse_reads.exists():
            raise FileNotFoundError(f"Reverse reads file not found: {reverse_reads}")
        
        # Build SPAdes command
        if mode == "isolate":
            command = f"spades.py --isolate"
        elif mode == "meta":
            command = f"metaspades.py"
        elif mode == "rna":
            command = f"rnaspades.py"
        else:
            logger.warning(f"Unknown mode '{mode}', using standard spades.py")
            command = "spades.py"
        
        # Add input files
        command += f" -1 {forward_reads}"
        if reverse_reads:
            command += f" -2 {reverse_reads}"
        
        # Add parameters
        command += f" -o {output_dir} -t {threads} -m {memory}"
        
        try:
            logger.info(f"Running command: {command}")
            code, stdout, stderr = self.executor.run_command(command, timeout=7200)
            logger.info(f"SPAdes assembly completed successfully. Output in {output_dir}")
            return True
        except Exception as e:
            logger.error(f"SPAdes assembly failed: {str(e)}")
            return False
    
    def get_assembly_stats(self, contigs_file: Path) -> Dict[str, any]:
        """
        Calculate basic statistics for an assembly.
        
        Args:
            contigs_file: Path to contigs FASTA file.
        
        Returns:
            Dictionary containing assembly statistics.
        
        Example:
            >>> assembler = GenomeAssembly()
            >>> stats = assembler.get_assembly_stats(Path("contigs.fasta"))
            >>> print(f"Total contigs: {stats['num_contigs']}")
        """
        logger.info(f"Calculating assembly statistics for: {contigs_file}")
        
        stats = {
            'num_contigs': 0,
            'total_length': 0,
            'longest_contig': 0,
            'shortest_contig': float('inf'),
            'n50': 0
        }
        
        if not contigs_file.exists():
            logger.warning(f"Contigs file not found: {contigs_file}")
            return stats
        
        try:
            contig_lengths = []
            current_length = 0
            
            with open(contigs_file, 'r') as f:
                for line in f:
                    if line.startswith('>'):
                        if current_length > 0:
                            contig_lengths.append(current_length)
                            current_length = 0
                        stats['num_contigs'] += 1
                    else:
                        current_length += len(line.strip())
                
                # Add last contig
                if current_length > 0:
                    contig_lengths.append(current_length)
            
            if contig_lengths:
                stats['total_length'] = sum(contig_lengths)
                stats['longest_contig'] = max(contig_lengths)
                stats['shortest_contig'] = min(contig_lengths)
                
                # Calculate N50
                contig_lengths.sort(reverse=True)
                half_total = stats['total_length'] / 2
                cumulative = 0
                for length in contig_lengths:
                    cumulative += length
                    if cumulative >= half_total:
                        stats['n50'] = length
                        break
            else:
                stats['shortest_contig'] = 0
            
            logger.info(f"Assembly statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating assembly statistics: {str(e)}")
            return stats
    
    def run_quast(
        self,
        contigs_file: Path,
        output_dir: Path,
        reference: Optional[Path] = None,
        threads: int = 1
    ) -> bool:
        """
        Run QUAST for assembly quality assessment.
        
        Args:
            contigs_file: Path to assembled contigs FASTA file.
            output_dir: Directory to store QUAST output.
            reference: Optional reference genome for comparison.
            threads: Number of threads to use (default: 1).
        
        Returns:
            True if QUAST completed successfully, False otherwise.
        
        Example:
            >>> assembler = GenomeAssembly()
            >>> assembler.run_quast(Path("contigs.fasta"), Path("quast_out"))
        """
        logger.info(f"Running QUAST on assembly: {contigs_file}")
        
        # Check if QUAST is available
        if not self.executor.check_tool_available("quast"):
            logger.warning("QUAST is not available. Skipping quality assessment.")
            return False
        
        if not contigs_file.exists():
            raise FileNotFoundError(f"Contigs file not found: {contigs_file}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build QUAST command
        command = f"quast {contigs_file} -o {output_dir} -t {threads}"
        
        if reference and reference.exists():
            command += f" -r {reference}"
        
        try:
            code, stdout, stderr = self.executor.run_command(command, timeout=1800)
            logger.info(f"QUAST completed successfully. Report in {output_dir}")
            return True
        except Exception as e:
            logger.error(f"QUAST failed: {str(e)}")
            return False
