"""
Core processing logic for genome analysis.
"""

from .command_executor import CommandExecutor
from .quality_control import QualityControl
from .assembly import GenomeAssembly

__all__ = ["CommandExecutor", "QualityControl", "GenomeAssembly"]
