from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from typing import Optional, List
import json

from document_parser.models import ParsedDocument, ParseRequest, ErrorResponse, ConfigurableField
from document_parser.config import settings, DEFAULT_CONFIGURABLE_FIELDS
from document_parser.pdf_processor import PDFProcessor
from document_parser.core import DocumentParser


app = FastAPI(
    title="Document Parser API",
    description="A document parsing platform that extracts structured data from PDF files using OpenAI",
    version="1.0.0"
)

# Initialize processors
pdf_processor = PDFProcessor()
document_parser = DocumentParser()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Document Parser API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model": settings.openai_model,
        "max_file_size_mb": settings.max_file_size_mb,
        "allowed_extensions": settings.allowed_extensions_list
    }


@app.get("/default-fields")
async def get_default_fields():
    """Get the list of default configurable fields"""
    return {"default_fields": DEFAULT_CONFIGURABLE_FIELDS}


@app.post("/parse", response_model=ParsedDocument)
async def parse_document(
    file: UploadFile = File(..., description="PDF file to parse"),
    custom_fields: Optional[str] = Form(None, description="JSON string of custom ConfigurableField objects"),
    extraction_instructions: Optional[str] = Form(None, description="Additional instructions for extraction")
):
    """
    Parse a PDF document and extract structured data

    Args:
        file: PDF file to parse
        custom_fields: Optional JSON string containing custom fields to extract
        extraction_instructions: Optional additional instructions for the LLM

    Returns:
        ParsedDocument with extracted fields
    """

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    try:
        # Read file content
        pdf_content = await file.read()

        # Check file size
        file_size_mb = len(pdf_content) / (1024 * 1024)
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
            )

        # Validate PDF
        if not pdf_processor.validate_pdf(pdf_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file"
            )

        # Extract text from PDF
        try:
            document_text = pdf_processor.extract_text_from_pdf(pdf_content)
            use_vision = False
        except Exception as text_error:
            # If text extraction fails, fall back to vision API
            print(f"Text extraction failed: {text_error}. Attempting vision processing...")
            try:
                base64_images = pdf_processor.convert_pdf_to_images(pdf_content)
                use_vision = True
            except Exception as vision_error:
                raise HTTPException(
                    status_code=422,
                    detail=f"Both text extraction and image conversion failed. Text error: {text_error}. Vision error: {vision_error}"
                )

        # Parse custom fields if provided
        configurable_fields = None
        if custom_fields:
            try:
                custom_fields_data = json.loads(custom_fields)
                configurable_fields = [
                    ConfigurableField(**field_data)
                    for field_data in custom_fields_data
                ]
            except (json.JSONDecodeError, ValueError) as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid custom_fields JSON: {str(e)}"
                )

        # Parse document
        if use_vision:
            parsed_result = document_parser.parse_document_images(
                base64_images=base64_images,
                configurable_fields=configurable_fields,
                extraction_instructions=extraction_instructions
            )
        else:
            parsed_result = document_parser.parse_document(
                document_text=document_text,
                configurable_fields=configurable_fields,
                extraction_instructions=extraction_instructions
            )

        return parsed_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )


@app.post("/parse-with-json", response_model=ParsedDocument)
async def parse_document_with_json(
    file: UploadFile = File(..., description="PDF file to parse"),
    parse_request: str = Form(..., description="JSON string of ParseRequest object")
):
    """
    Alternative endpoint that accepts a full ParseRequest as JSON

    Args:
        file: PDF file to parse
        parse_request: JSON string containing ParseRequest data

    Returns:
        ParsedDocument with extracted fields
    """

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    try:
        # Parse request data
        try:
            request_data = json.loads(parse_request)
            parse_req = ParseRequest(**request_data)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid parse_request JSON: {str(e)}"
            )

        # Read file content
        pdf_content = await file.read()

        # Check file size
        file_size_mb = len(pdf_content) / (1024 * 1024)
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
            )

        # Validate PDF
        if not pdf_processor.validate_pdf(pdf_content):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file"
            )

        # Extract text from PDF
        document_text = pdf_processor.extract_text_from_pdf(pdf_content)

        # Parse document
        parsed_result = document_parser.parse_document(
            document_text=document_text,
            configurable_fields=parse_req.custom_fields,
            extraction_instructions=parse_req.extraction_instructions
        )

        return parsed_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )
