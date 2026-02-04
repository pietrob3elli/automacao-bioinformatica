"""
Bioinformatics Pipeline Package
"""

__version__ = '1.0.0'
__author__ = 'Pietro Belli'

from .genome_assembly import GenomeAssembler
from .data_visualization import DataVisualizer

__all__ = ['GenomeAssembler', 'DataVisualizer']
