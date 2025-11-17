"""
Structured logging configuration for v7.5-main Layout Builder

Provides centralized logging for:
- Storage operations (filesystem, Supabase)
- API requests and responses
- Cache operations
- Error tracking

Usage:
    from logger import get_logger

    logger = get_logger(__name__)
    logger.info("Presentation created", presentation_id=pres_id)
    logger.error("Storage error", error=str(e), operation="save")
"""

import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import json


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter for structured JSON logging

    Outputs logs in JSON format for easier parsing and analysis:
    {
        "timestamp": "2025-11-16T10:30:00.000Z",
        "level": "INFO",
        "logger": "storage",
        "message": "Presentation saved",
        "presentation_id": "uuid-here",
        "storage_backend": "supabase"
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON

        Args:
            record: Log record to format

        Returns:
            JSON string with structured log data
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add any extra fields passed to logger
        # Example: logger.info("message", key=value)
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class ExtraFieldsAdapter(logging.LoggerAdapter):
    """
    Adapter to support extra fields in log messages

    Allows passing additional context as keyword arguments:
    logger.info("Saved presentation", presentation_id=id, backend="supabase")
    """

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """
        Process log message and extract extra fields

        Args:
            msg: Log message
            kwargs: Keyword arguments (may contain 'extra_fields')

        Returns:
            Tuple of (message, modified kwargs)
        """
        # Extract extra fields from kwargs
        extra_fields = {}
        keys_to_remove = []

        for key, value in kwargs.items():
            if key not in ['exc_info', 'stack_info', 'stacklevel', 'extra']:
                extra_fields[key] = value
                keys_to_remove.append(key)

        # Remove extra fields from kwargs (they're not standard logging params)
        for key in keys_to_remove:
            kwargs.pop(key, None)

        # Add extra fields to the record
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra']['extra_fields'] = extra_fields

        return msg, kwargs


# ==================== Logger Configuration ====================

def get_logger(name: str, level: Optional[str] = None) -> logging.LoggerAdapter:
    """
    Get configured logger instance with structured logging

    Args:
        name: Logger name (typically __name__ from calling module)
        level: Optional log level override (DEBUG, INFO, WARNING, ERROR)
               If not provided, uses INFO in production, DEBUG in development

    Returns:
        Logger adapter with extra fields support

    Example:
        logger = get_logger(__name__)
        logger.info("Operation started", operation="save", presentation_id=id)
        logger.error("Operation failed", error=str(e), operation="save")
    """
    logger = logging.getLogger(name)

    # Set log level
    if level:
        logger.setLevel(getattr(logging, level.upper()))
    else:
        # Default to INFO (can be overridden by environment variable)
        import os
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Use structured JSON formatter
    formatter = StructuredFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Return adapter for extra fields support
    return ExtraFieldsAdapter(logger, {})


# ==================== Convenience Loggers ====================

def get_storage_logger() -> logging.LoggerAdapter:
    """
    Get logger for storage operations

    Returns:
        Configured logger for storage module
    """
    return get_logger("storage")


def get_server_logger() -> logging.LoggerAdapter:
    """
    Get logger for server/API operations

    Returns:
        Configured logger for server module
    """
    return get_logger("server")


def get_cache_logger() -> logging.LoggerAdapter:
    """
    Get logger for cache operations

    Returns:
        Configured logger for cache module
    """
    return get_logger("cache")


# ==================== Log Level Utilities ====================

def set_log_level(level: str):
    """
    Set global log level for all loggers

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Example:
        set_log_level("DEBUG")  # Enable debug logging
    """
    logging.getLogger().setLevel(getattr(logging, level.upper()))


def enable_debug_logging():
    """Enable debug logging (verbose output)"""
    set_log_level("DEBUG")


def enable_info_logging():
    """Enable info logging (normal output)"""
    set_log_level("INFO")


# ==================== Testing & Debugging ====================

if __name__ == "__main__":
    """Test structured logging"""

    # Test basic logging
    logger = get_logger(__name__)
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")

    # Test with extra fields
    logger.info("Presentation saved",
                presentation_id="test-123",
                backend="supabase",
                duration_ms=150)

    # Test error with exception
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.error("Operation failed",
                    operation="test",
                    error=str(e),
                    exc_info=True)

    # Test different log levels
    logger.debug("Debug message (may not appear if INFO level)")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    print("\n--- Testing convenience loggers ---")
    storage_logger = get_storage_logger()
    storage_logger.info("Storage operation", operation="save", backend="filesystem")

    server_logger = get_server_logger()
    server_logger.info("API request", method="POST", endpoint="/api/presentations")

    cache_logger = get_cache_logger()
    cache_logger.info("Cache operation", operation="get", hit=True, key="pres-123")
