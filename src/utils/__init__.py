"""
Centralized logging configuration using Loguru.
Provides structured, colored, and file-based logging with automatic rotation.
"""

from loguru import logger
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import os

class GestLogger:
    """
    Centralized logger for the Gest application using Loguru.
    Provides console and file logging with automatic rotation and formatting.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the logger with configuration.
        
        Args:
            config: Logging configuration dictionary
        """
        self.config = config or self._get_default_config()
        self._setup_logger()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default logging configuration."""
        return {
            "log_dir": "logs",
            "max_file_size": "10MB",
            "backup_count": 5,
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            "level": "INFO"
        }
    
    def _setup_logger(self) -> None:
        """Setup the Loguru logger with console and file handlers."""
        # Remove default handler
        logger.remove()
        
        # Create logs directory
        log_dir = Path(self.config["log_dir"])
        log_dir.mkdir(exist_ok=True)
        
        # Console handler with colors
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            level=self.config["level"],
            colorize=True
        )
        
        # File handler for all logs
        logger.add(
            log_dir / "gest_{time}.log",
            format=self.config["format"],
            level="DEBUG",
            rotation=self.config["max_file_size"],
            retention=self.config["backup_count"],
            compression="zip"
        )
        
        # Separate error log
        logger.add(
            log_dir / "gest_errors_{time}.log",
            format=self.config["format"],
            level="ERROR",
            rotation=self.config["max_file_size"],
            retention=self.config["backup_count"],
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        logger.info("Logger initialized successfully")
    
    def get_logger(self):
        """Get the configured logger instance."""
        return logger

# Global logger instance
_logger_instance = None

def setup_logger(config: Optional[Dict[str, Any]] = None):
    """
    Setup and return the global logger instance.
    
    Args:
        config: Optional logging configuration
        
    Returns:
        Configured logger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = GestLogger(config)
    return _logger_instance.get_logger()

def get_logger():
    """
    Get the global logger instance.
    
    Returns:
        Logger instance
    """
    if _logger_instance is None:
        return setup_logger()
    return _logger_instance.get_logger()

# Export logger for direct import
__all__ = ["setup_logger", "get_logger", "logger"]
