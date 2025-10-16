"""Sistema logging centralizzato."""

import logging
import sys
from pathlib import Path


def setup_logger(name: str = "pythonita", level=logging.INFO, log_file=None):
    """
    Setup logger centralizzato.
    
    Args:
        name: Nome logger
        level: Livello logging
        log_file: Path file log (opzionale)
    
    Returns:
        Logger configurato
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicati
    if logger.handlers:
        return logger
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (se richiesto)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

