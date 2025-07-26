#!/usr/bin/env python3
"""
Simple CLI tool for testing the document parser
"""

import argparse
import asyncio
import aiohttp
import json
from pathlib import Path


async def parse_document(file_path: str, custom_fields_file: str = None, instructions: str = None):
    """Parse a document using the API"""

    if not Path(file_path).exists():
        print(f"Error: File {file_path} not found")
        return

    base_url = "http://localhost:8000"

    async with aiohttp.ClientSession() as session:
        # Prepare form data
        data = aiohttp.FormData()

        # Add file
        file_path_obj = Path(file_path)
        with open(file_path_obj, 'rb') as f:
            file_content = f.read()
            data.add_field('file', file_content, filename=file_path_obj.name, content_type='application/pdf')

        # Add custom fields if provided
        if custom_fields_file:
            if Path(custom_fields_file).exists():
                with open(custom_fields_file, 'r') as f:
                    custom_fields = f.read()
                data.add_field('custom_fields', custom_fields)
            else:
                print(f"Warning: Custom fields file {custom_fields_file} not found")

        # Add instructions if provided
        if instructions:
            data.add_field('extraction_instructions', instructions)

        # Make request
        try:
            async with session.post(f"{base_url}/parse", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("Document parsed successfully!")
                    print("=" * 50)

                    print("\\nConfigurable Fields:")
                    for field, value in result['configurable_fields'].items():
                        print(f"  {field}: {value}")

                    print("\\nDiscovered Fields:")
                    for field, value in result['discovered_fields'].items():
                        print(f"  {field}: {value}")

                    if result.get('confidence_score'):
                        print(f"\\nConfidence Score: {result['confidence_score']}")

                    if result.get('processing_notes'):
                        print(f"\\nProcessing Notes: {result['processing_notes']}")

                else:
                    error_data = await response.json()
                    print(f"Error {response.status}: {error_data.get('detail', 'Unknown error')}")

        except aiohttp.ClientConnectorError:
            print("Error: Could not connect to the server. Make sure it's running on http://localhost:8000")
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Document Parser CLI Tool")
    parser.add_argument("file", help="Path to PDF file to parse")
    parser.add_argument("--custom-fields", help="Path to JSON file with custom fields")
    parser.add_argument("--instructions", help="Additional extraction instructions")

    args = parser.parse_args()

    asyncio.run(parse_document(args.file, args.custom_fields, args.instructions))


if __name__ == "__main__":
    main()
