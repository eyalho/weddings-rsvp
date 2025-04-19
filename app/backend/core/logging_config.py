"""
Logging configuration module.

Provides simple, clean logging setup following:
- "Simple is better than complex"
- "Explicit is better than implicit"
- "Readability counts"
"""
import sys
import logging
import os
from typing import Optional, Union, Dict, Any

from .config import LogLevel


def configure_logging(
    level: Optional[Union[LogLevel, str]] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
) -> None:
    """
    Configure application logging with sensible defaults.
    
    This function deliberately avoids complexity, providing a 
    simple setup for the common case while allowing customization.
    
    Args:
        level: The log level (string or LogLevel enum)
        log_format: Custom log format string
        date_format: Custom date format string
    """
    # Use simple default values - "Simple is better than complex"
    if level is None:
        level = LogLevel.INFO
        
    # Convert enum to string if needed
    if isinstance(level, LogLevel):
        level_str = level.value
    else:
        level_str = str(level)
        
    # Simple defaults - "Readability counts"
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
    if date_format is None:
        date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger with sane defaults
    logging.basicConfig(
        level=level_str,
        format=log_format,
        datefmt=date_format,
        stream=sys.stdout,
        force=True,  # Override any existing configuration
    )
    
    # Simple feedback about logging setup
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured: level={level_str}")
    
    # Set external library logging levels to avoid noise
    for noisy_logger in ['urllib3', 'elasticsearch', 'requests']:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with a specific name.
    
    Simple utility that makes logger creation more explicit.
    
    Args:
        name: Logger name, typically __name__
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name) 