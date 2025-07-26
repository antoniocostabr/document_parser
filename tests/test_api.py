import asyncio
import aiohttp
import json
import pytest
from pathlib import Path


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test the health check endpoint"""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/health") as response:
            assert response.status == 200
            data = await response.json()
            assert "status" in data
            assert data["status"] == "healthy"
            assert "model" in data
            assert "max_file_size_mb" in data
            assert "allowed_extensions" in data


@pytest.mark.asyncio
async def test_default_fields_endpoint():
    """Test the default fields endpoint"""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/default-fields") as response:
            assert response.status == 200
            data = await response.json()
            assert "default_fields" in data
            assert isinstance(data["default_fields"], list)
            assert len(data["default_fields"]) > 0
            
            # Check first field structure
            field = data["default_fields"][0]
            assert "name" in field
            assert "description" in field
            assert "data_type" in field


@pytest.mark.asyncio
async def test_parse_endpoint_with_text_pdf():
    """Test the parse endpoint with a text-based PDF"""
    base_url = "http://localhost:8000"
    pdf_path = Path("data/test_invoice.pdf")
    
    if not pdf_path.exists():
        pytest.skip("Test PDF file not found")
    
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        with open(pdf_path, 'rb') as f:
            data.add_field('file', f.read(), filename=pdf_path.name, content_type='application/pdf')
        
        async with session.post(f"{base_url}/parse", data=data) as response:
            assert response.status == 200
            result = await response.json()
            
            # Check response structure
            assert "configurable_fields" in result
            assert "discovered_fields" in result
            assert "confidence_score" in result
            assert "processing_notes" in result
            
            # Check confidence score is valid
            assert 0 <= result["confidence_score"] <= 1


@pytest.mark.asyncio
async def test_parse_endpoint_with_image_pdf():
    """Test the parse endpoint with an image-based PDF (CNH document)"""
    base_url = "http://localhost:8000"
    pdf_path = Path("data/2 - CNH - ANTONIO CRISTIANO.pdf")
    
    if not pdf_path.exists():
        pytest.skip("CNH test PDF file not found")
    
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        with open(pdf_path, 'rb') as f:
            data.add_field('file', f.read(), filename=pdf_path.name, content_type='application/pdf')
        
        async with session.post(f"{base_url}/parse", data=data) as response:
            assert response.status == 200
            result = await response.json()
            
            # Check response structure
            assert "configurable_fields" in result
            assert "discovered_fields" in result
            assert "confidence_score" in result
            assert "processing_notes" in result
            
            # Check specific fields for CNH document
            configurable = result["configurable_fields"]
            assert configurable["document_type"] is not None
            assert configurable["person_name"] is not None
            assert result["confidence_score"] >= 0.8  # Should be high confidence


@pytest.mark.asyncio
async def test_parse_endpoint_with_custom_fields():
    """Test the parse endpoint with custom fields"""
    base_url = "http://localhost:8000"
    pdf_path = Path("data/test_invoice.pdf")
    
    if not pdf_path.exists():
        pytest.skip("Test PDF file not found")
    
    custom_fields = [
        {
            "name": "invoice_number",
            "description": "The unique invoice number",
            "data_type": "string"
        },
        {
            "name": "total_amount",
            "description": "The total amount",
            "data_type": "number"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        with open(pdf_path, 'rb') as f:
            data.add_field('file', f.read(), filename=pdf_path.name, content_type='application/pdf')
        data.add_field('custom_fields', json.dumps(custom_fields))
        data.add_field('extraction_instructions', 'Focus on invoice details')
        
        async with session.post(f"{base_url}/parse", data=data) as response:
            assert response.status == 200
            result = await response.json()
            
            # Check that custom fields are in response
            configurable = result["configurable_fields"]
            assert "invoice_number" in configurable
            assert "total_amount" in configurable


def test_create_example_files():
    """Test creation of example files"""
    # Example custom fields
    custom_fields_example = [
        {
            "name": "invoice_number",
            "description": "Invoice or bill number",
            "data_type": "string"
        },
        {
            "name": "due_date", 
            "description": "Payment due date",
            "data_type": "date"
        },
        {
            "name": "total_amount",
            "description": "Total amount due",
            "data_type": "number"
        }
    ]

    # Example parse request
    parse_request_example = {
        "custom_fields": custom_fields_example,
        "extraction_instructions": "Focus on financial information and payment details. Extract all monetary amounts found in the document."
    }

    # Save examples
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)

    with open(examples_dir / "custom_fields_example.json", "w") as f:
        json.dump(custom_fields_example, f, indent=2)

    with open(examples_dir / "parse_request_example.json", "w") as f:
        json.dump(parse_request_example, f, indent=2)

    # Verify files were created
    assert (examples_dir / "custom_fields_example.json").exists()
    assert (examples_dir / "parse_request_example.json").exists()


@pytest.mark.asyncio
async def test_document_parser():
    """Test the document parser API"""

    base_url = "http://localhost:8000"

    async with aiohttp.ClientSession() as session:

        # Test health check
        print("Testing health check...")
        async with session.get(f"{base_url}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Health check passed: {data}")
            else:
                print(f"✗ Health check failed: {response.status}")
                return

        # Test default fields endpoint
        print("\\nTesting default fields...")
        async with session.get(f"{base_url}/default-fields") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Default fields retrieved: {len(data['default_fields'])} fields")
                for field in data['default_fields'][:3]:  # Show first 3 fields
                    print(f"  - {field['name']}: {field['description']}")
            else:
                print(f"✗ Default fields test failed: {response.status}")

        # Note: PDF parsing test would require an actual PDF file
        print("\\n📝 To test PDF parsing:")
        print("1. Start the server: python main.py")
        print("2. Upload a PDF file to /parse endpoint")
        print("3. Check the extracted configurable_fields and discovered_fields")


def create_test_request_examples():
    """Create example request files for testing"""

    # Example custom fields
    custom_fields_example = [
        {
            "name": "invoice_number",
            "description": "Invoice or bill number",
            "data_type": "string"
        },
        {
            "name": "due_date",
            "description": "Payment due date",
            "data_type": "date"
        },
        {
            "name": "total_amount",
            "description": "Total amount due",
            "data_type": "number"
        }
    ]

    # Example parse request
    parse_request_example = {
        "custom_fields": custom_fields_example,
        "extraction_instructions": "Focus on financial information and payment details. Extract all monetary amounts found in the document."
    }

    # Save examples
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)

    with open(examples_dir / "custom_fields_example.json", "w") as f:
        json.dump(custom_fields_example, f, indent=2)

    with open(examples_dir / "parse_request_example.json", "w") as f:
        json.dump(parse_request_example, f, indent=2)

    print("Created example files in 'examples/' directory:")
    print("- custom_fields_example.json")
    print("- parse_request_example.json")


if __name__ == "__main__":
    print("Document Parser Test Suite")
    print("=" * 40)

    # Create example files
    create_test_request_examples()
    print()

    # Run async tests
    asyncio.run(test_document_parser())
