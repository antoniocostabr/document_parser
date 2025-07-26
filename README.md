# Document Parser Platform

A Python-based document parsing platform that uses OpenAI to extract structured data from PDF files. The platform provides both a REST API and a command-line interface.

## Features

- **Intelligent PDF Parsing**: Extract structured data from PDF documents using OpenAI's GPT models
- **Configurable Fields**: Define custom fields to extract based on your requirements
- **Discovery Mode**: Automatically discover and extract additional fields found in documents
- **Confidence Scoring**: Get confidence scores for extraction accuracy
- **REST API**: Easy-to-use API for programmatic access
- **Command Line Interface**: Simple CLI for quick document processing
- **Docker Support**: Containerized deployment ready

## Project Structure

```
document_parser/
├── document_parser/          # Core parsing functionality
│   ├── __init__.py
│   ├── config.py            # Configuration and settings
│   ├── core.py              # Main DocumentParser class
│   ├── models.py            # Pydantic models for data validation
│   └── pdf_processor.py     # PDF processing utilities
├── api/                     # FastAPI web application
│   ├── __init__.py
│   └── main.py             # API endpoints and routes
├── cli/                     # Command-line interface
│   ├── __init__.py
│   └── main.py             # CLI implementation
├── tests/                   # Test suite
│   └── test_api.py
├── scripts/                 # Utility scripts
│   ├── generate_sample_pdfs.py
│   └── create_poor_quality_pdf.py
├── test_files/             # Sample test documents
├── examples/               # Example configuration files
├── app.py                  # Main server entry point
├── parse.py               # CLI entry point
└── setup.py               # Package configuration
```

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd document_parser
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Running the Application

#### Quick Start with Makefile
The project includes a comprehensive Makefile for easy development and deployment:

```bash
# Show all available commands
make help

# Complete setup (install dependencies + generate test files)
make setup

# Start development server
make dev

# Build and deploy with Docker Compose
make deploy
```

#### Manual Setup

##### Start the API Server
```bash
python app.py
```

The API will be available at `http://localhost:8000`

##### Use the CLI
```bash
python parse.py path/to/your/document.pdf
```

### API Endpoints

- `GET /health` - Health check and system information
- `GET /default-fields` - Get default configurable fields
- `POST /parse` - Parse a PDF document

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Parse a document
curl -X POST \
  -F "file=@sample.pdf" \
  -F "custom_fields=[{\"name\":\"invoice_number\",\"description\":\"The invoice number\",\"required\":true}]" \
  http://localhost:8000/parse
```

## Makefile Commands

The project includes a comprehensive Makefile with commands for development, testing, and deployment:

### Development Commands
```bash
make setup          # Complete setup: install dependencies and generate test files
make dev             # Start development server
make dev-cli         # Test CLI with sample invoice
make install         # Install dependencies and setup virtual environment
make clean           # Clean up temporary files and cache
```

### Testing Commands
```bash
make test            # Run tests
make test-api        # Test API endpoints (requires running server)
make parse-test      # Quick parse test with sample files
make health          # Check API health
make full-test       # Full test: start compose, test API, stop compose
```

### Docker Commands
```bash
make docker-build    # Build Docker image
make docker-run      # Run Docker container with env file
make docker-stop     # Stop and remove Docker container
make docker-logs     # Show Docker container logs
make docker-shell    # Open shell in running Docker container
```

### Docker Compose Commands
```bash
make compose-up      # Start services with Docker Compose
make compose-down    # Stop services with Docker Compose
make compose-logs    # Show Docker Compose logs
make compose-ps      # Show Docker Compose service status
make deploy          # Build and deploy with Docker Compose
```

### Utility Commands
```bash
make env-check       # Check environment variables
make generate-samples # Generate sample PDF files for testing
make shell           # Start Python shell with project context
```

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 10)

## Package Installation

You can install the package in development mode:
```bash
pip install -e .
```

This allows you to import and use the document parser in other Python projects:
```python
from document_parser import DocumentParser
from document_parser.models import ConfigurableField

# Use the parser in your code
parser = DocumentParser()
result = parser.parse_document(pdf_content, custom_fields)
```

## Docker Support

### Using Makefile (Recommended)
```bash
# Build and deploy with Docker Compose
make deploy

# Or step by step
make docker-build    # Build the image
make compose-up      # Start with Docker Compose
make compose-down    # Stop services
```

### Manual Docker Commands

#### Build and run with Docker:
```bash
docker build -t document-parser .
docker run -p 8000:8000 --env-file .env document-parser
```

#### Or use Docker Compose:
```bash
docker-compose up
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Development

The project includes sample PDF generation scripts for testing:
```bash
python scripts/generate_sample_pdfs.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
