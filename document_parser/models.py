from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class ConfigurableField(BaseModel):
    """Represents a configurable field that should be extracted from documents"""
    name: str
    description: str
    data_type: str = "string"  # string, number, date, boolean
    required: bool = False


class ParsedDocument(BaseModel):
    """Response model for parsed document"""
    configurable_fields: Dict[str, Optional[Any]]
    discovered_fields: Dict[str, Any]
    confidence_score: Optional[float] = None
    processing_notes: Optional[str] = None


class ParseRequest(BaseModel):
    """Request model for document parsing"""
    custom_fields: Optional[List[ConfigurableField]] = None
    extraction_instructions: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None
