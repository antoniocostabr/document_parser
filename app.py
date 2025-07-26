#!/usr/bin/env python3
"""
Main entry point for the Document Parser API server
"""

import uvicorn
from api.main import app
from document_parser.config import settings


def main():
    """Start the Document Parser API server"""
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()
