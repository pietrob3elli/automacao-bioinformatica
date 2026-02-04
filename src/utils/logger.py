"""
Logger configuration for the bioinformatics pipeline.

This module provides logging configuration with proper formatting and handlers.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "bioinformatics_pipeline",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure and return a logger with file and/or console handlers.
    
    Args:
        name: Name of the logger (default: 'bioinformatics_pipeline').
        level: Logging level (default: logging.INFO).
        log_file: Optional path to log file. If None, no file logging.
        console: If True, also log to console (default: True).
    
    Returns:
        Configured logger instance.
    
    Example:
        >>> logger = setup_logger(
        ...     name="my_analysis",
        ...     level=logging.DEBUG,
        ...     log_file=Path("analysis.log")
        ... )
        >>> logger.info("Analysis started")
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if log_file is provided
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info(f"Logger '{name}' initialized at level {logging.getLevelName(level)}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger by name.
    
    Args:
        name: Name of the logger to retrieve.
    
    Returns:
        Logger instance.
    
    Example:
        >>> logger = get_logger("bioinformatics_pipeline")
        >>> logger.info("Using existing logger")
    """
    return logging.getLogger(name)
