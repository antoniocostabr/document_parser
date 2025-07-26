import asyncio
import aiohttp
import json
from pathlib import Path


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
