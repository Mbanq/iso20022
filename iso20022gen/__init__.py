"""
ISO 20022 Python package for generating ISO 20022 messages.

This package provides functionality for generating ISO 20022 compliant
XML messages from JSON payloads.
"""

__version__ = "0.1.0"

# Import only the configure function, not the entire module
from iso20022gen.config import configure

__all__ = ["Iso20022CodeGen", "configure"] 