"""
File I/O utilities for reading and processing data files.

This module provides utilities for reading CSV/TSV files and other
common bioinformatics file formats.
"""

import logging
import csv
from pathlib import Path
from typing import List, Dict, Optional, Union, Any


logger = logging.getLogger(__name__)


class FileHandler:
    """
    Handle file I/O operations for the pipeline.
    
    This class provides methods for reading and writing various file formats
    commonly used in bioinformatics.
    """
    
    @staticmethod
    def read_csv(
        file_path: Path,
        delimiter: str = ',',
        has_header: bool = True
    ) -> List[Dict[str, str]]:
        """
        Read a CSV or TSV file and return data as a list of dictionaries.
        
        Args:
            file_path: Path to the CSV/TSV file.
            delimiter: Field delimiter (default: ',').
            has_header: If True, first row is treated as header (default: True).
        
        Returns:
            List of dictionaries where keys are column names.
        
        Raises:
            FileNotFoundError: If the file doesn't exist.
        
        Example:
            >>> handler = FileHandler()
            >>> data = handler.read_csv(Path("results.csv"))
            >>> for row in data:
            ...     print(row['sample_name'], row['quality_score'])
        """
        logger.info(f"Reading CSV/TSV file: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        data = []
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                if has_header:
                    reader = csv.DictReader(f, delimiter=delimiter)
                    data = list(reader)
                else:
                    reader = csv.reader(f, delimiter=delimiter)
                    data = [{'col_' + str(i): val for i, val in enumerate(row)} 
                           for row in reader]
            
            logger.info(f"Successfully read {len(data)} rows from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_csv(
        data: List[Dict[str, Any]],
        file_path: Path,
        delimiter: str = ',',
        fieldnames: Optional[List[str]] = None
    ) -> bool:
        """
        Write data to a CSV or TSV file.
        
        Args:
            data: List of dictionaries to write.
            file_path: Path to output file.
            delimiter: Field delimiter (default: ',').
            fieldnames: Optional list of field names for header.
                       If None, uses keys from first dict.
        
        Returns:
            True if write was successful, False otherwise.
        
        Example:
            >>> handler = FileHandler()
            >>> data = [
            ...     {'sample': 'S1', 'reads': '1000000'},
            ...     {'sample': 'S2', 'reads': '1200000'}
            ... ]
            >>> handler.write_csv(data, Path("output.csv"))
        """
        logger.info(f"Writing CSV/TSV file: {file_path}")
        
        if not data:
            logger.warning("No data to write")
            return False
        
        try:
            # Create parent directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get fieldnames
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Successfully wrote {len(data)} rows to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def read_fasta(file_path: Path) -> Dict[str, str]:
        """
        Read a FASTA file and return sequences as a dictionary.
        
        Args:
            file_path: Path to FASTA file.
        
        Returns:
            Dictionary mapping sequence IDs to sequences.
        
        Example:
            >>> handler = FileHandler()
            >>> sequences = handler.read_fasta(Path("genome.fasta"))
            >>> for seq_id, sequence in sequences.items():
            ...     print(f"{seq_id}: {len(sequence)} bp")
        """
        logger.info(f"Reading FASTA file: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        sequences = {}
        current_id = None
        current_seq = []
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('>'):
                        # Save previous sequence if exists
                        if current_id:
                            sequences[current_id] = ''.join(current_seq)
                        # Start new sequence
                        current_id = line[1:].split()[0]
                        current_seq = []
                    else:
                        current_seq.append(line)
                
                # Save last sequence
                if current_id:
                    sequences[current_id] = ''.join(current_seq)
            
            logger.info(f"Successfully read {len(sequences)} sequences from {file_path}")
            return sequences
            
        except Exception as e:
            logger.error(f"Error reading FASTA file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_fasta(
        sequences: Dict[str, str],
        file_path: Path,
        line_width: int = 80
    ) -> bool:
        """
        Write sequences to a FASTA file.
        
        Args:
            sequences: Dictionary mapping sequence IDs to sequences.
            file_path: Path to output FASTA file.
            line_width: Maximum line width for sequences (default: 80).
        
        Returns:
            True if write was successful, False otherwise.
        
        Example:
            >>> handler = FileHandler()
            >>> sequences = {'contig1': 'ATCGATCG', 'contig2': 'GCTAGCTA'}
            >>> handler.write_fasta(sequences, Path("output.fasta"))
        """
        logger.info(f"Writing FASTA file: {file_path}")
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                for seq_id, sequence in sequences.items():
                    f.write(f">{seq_id}\n")
                    
                    # Write sequence in lines of line_width
                    for i in range(0, len(sequence), line_width):
                        f.write(sequence[i:i + line_width] + '\n')
            
            logger.info(f"Successfully wrote {len(sequences)} sequences to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing FASTA file {file_path}: {str(e)}")
            return False
