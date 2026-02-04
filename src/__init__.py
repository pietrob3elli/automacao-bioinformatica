"""
"""
Bioinformatics Automation Pipeline
A modular Python pipeline for prokaryotic genome analysis.
"""

__version__ = "1.0.0"
__author__ = "pietrob3elli"

from .genome_assembly import GenomeAssembler
from .data_visualization import DataVisualizer

# Define o que será exportado ao importar o pacote
__all__ = ['GenomeAssembler', 'DataVisualizer']
