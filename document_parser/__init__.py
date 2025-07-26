"""
Document Parser Package

A Python package for extracting structured data from PDF documents using OpenAI.
"""

__version__ = "1.0.0"
__author__ = "Document Parser Team"

from .core import DocumentParser
from .pdf_processor import PDFProcessor
from .models import ParsedDocument, ConfigurableField, ParseRequest

__all__ = [
    "DocumentParser",
    "PDFProcessor",
    "ParsedDocument",
    "ConfigurableField",
    "ParseRequest",
]
