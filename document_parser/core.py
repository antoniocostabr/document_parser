import openai
import json
from typing import Dict, Any, List, Optional
from .models import ConfigurableField, ParsedDocument
from .config import settings, DEFAULT_CONFIGURABLE_FIELDS


class DocumentParser:
    """Handles document parsing using OpenAI API"""

    def __init__(self):
        # Initialize client as None - will create when needed
        self.client = None

    def _get_client(self):
        """Get or create OpenAI client"""
        if self.client is None:
            try:
                # Simple client initialization without extra parameters
                self.client = openai.OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                raise Exception(f"Failed to initialize OpenAI client: {str(e)}")
        return self.client

    def parse_document(
        self,
        document_text: str,
        configurable_fields: Optional[List[ConfigurableField]] = None,
        extraction_instructions: Optional[str] = None
    ) -> ParsedDocument:
        """
        Parse document text using OpenAI API

        Args:
            document_text: Text content of the document
            configurable_fields: List of fields to extract (uses defaults if None)
            extraction_instructions: Additional instructions for extraction

        Returns:
            ParsedDocument with extracted fields
        """
        if configurable_fields is None:
            configurable_fields = DEFAULT_CONFIGURABLE_FIELDS

        # Build the prompt
        prompt = self._build_extraction_prompt(
            document_text,
            configurable_fields,
            extraction_instructions
        )

        try:
            client = self._get_client()

            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert document parser. Extract information accurately and return it in the specified JSON format."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=2000
            )

            # Parse the response
            response_text = response.choices[0].message.content
            parsed_response = self._parse_llm_response(response_text, configurable_fields)

            return parsed_response

        except Exception as e:
            raise Exception(f"Failed to parse document with OpenAI: {str(e)}")

    def parse_document_images(
        self,
        base64_images: List[str],
        configurable_fields: Optional[List[ConfigurableField]] = None,
        extraction_instructions: Optional[str] = None
    ) -> ParsedDocument:
        """
        Parse document from images using OpenAI Vision API

        Args:
            base64_images: List of base64-encoded images (one per page)
            configurable_fields: List of fields to extract (uses defaults if None)
            extraction_instructions: Additional instructions for extraction

        Returns:
            ParsedDocument with extracted fields
        """
        if configurable_fields is None:
            configurable_fields = DEFAULT_CONFIGURABLE_FIELDS

        # Build the extraction instructions
        fields_description = "\\n".join([
            f"- {field.name} ({field.data_type}): {field.description}"
            for field in configurable_fields
        ])

        # Create the text prompt
        text_prompt = f"""
Please analyze the document images and extract information according to these requirements:

CONFIGURABLE FIELDS TO EXTRACT:
{fields_description}

INSTRUCTIONS:
1. Extract values for the configurable fields listed above. If a field is not found in the document, set its value to null.
2. Additionally, identify and extract any other relevant information you find in the document that might be valuable.
3. Provide YOUR OWN confidence score between 0.0 and 1.0 based on your assessment of:
   - How clear and readable the document images are
   - How certain you are about the field value matches
   - How complete your extraction is
   - Overall document quality and structure
4. Return the response in the following JSON format:

{{
    "configurable_fields": {{
        "field_name": "extracted_value_or_null"
    }},
    "discovered_fields": {{
        "other_field_name": "extracted_value"
    }},
    "confidence_score": <number_between_0_and_1>,
    "processing_notes": "Any relevant notes about the extraction process"
}}

{f"ADDITIONAL INSTRUCTIONS: {extraction_instructions}" if extraction_instructions else ""}
"""

        try:
            client = self._get_client()

            # Prepare the message content with images
            content = [{"type": "text", "text": text_prompt}]
            
            # Add each image to the content
            for img_base64 in base64_images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}",
                        "detail": "high"
                    }
                })

            response = client.chat.completions.create(
                model="gpt-4o",  # Use vision-capable model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert document parser. Analyze document images and extract information accurately, returning it in the specified JSON format."
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=2000
            )

            # Parse the response
            response_text = response.choices[0].message.content
            parsed_response = self._parse_llm_response(response_text, configurable_fields)

            return parsed_response

        except Exception as e:
            raise Exception(f"Failed to parse document images with OpenAI Vision: {str(e)}")

    def _build_extraction_prompt(
        self,
        document_text: str,
        configurable_fields: List[ConfigurableField],
        extraction_instructions: Optional[str] = None
    ) -> str:
        """Build the extraction prompt for OpenAI"""

        # Build configurable fields description
        fields_description = "\\n".join([
            f"- {field.name} ({field.data_type}): {field.description}"
            for field in configurable_fields
        ])

        prompt = f"""
Please analyze the following document and extract information according to these requirements:

CONFIGURABLE FIELDS TO EXTRACT:
{fields_description}

DOCUMENT TEXT:
{document_text}

INSTRUCTIONS:
1. Extract values for the configurable fields listed above. If a field is not found in the document, set its value to null.
2. Additionally, identify and extract any other relevant information you find in the document that might be valuable.
3. Provide YOUR OWN confidence score between 0.0 and 1.0 based on your assessment of:
   - How clear and readable the document text was
   - How certain you are about the field value matches
   - How complete your extraction is
   - Overall document quality and structure
4. Return the response in the following JSON format:

{{
    "configurable_fields": {{
        "field_name": "extracted_value_or_null"
    }},
    "discovered_fields": {{
        "other_field_name": "extracted_value"
    }},
    "confidence_score": <number_between_0_and_1>,
    "processing_notes": "Any relevant notes about the extraction process"
}}

ADDITIONAL EXTRACTION INSTRUCTIONS:
{extraction_instructions or "None"}

Please ensure the JSON is valid and complete. For dates, use ISO format (YYYY-MM-DD). For amounts, extract numeric values without currency symbols.

IMPORTANT: Generate a genuine confidence score based on your actual assessment - do not use example values!
"""
        return prompt

    def _parse_llm_response(
        self,
        response_text: str,
        configurable_fields: List[ConfigurableField]
    ) -> ParsedDocument:
        """Parse the LLM response into a ParsedDocument"""

        try:
            # Try to extract JSON from the response
            response_text = response_text.strip()

            # Handle cases where the response might have markdown formatting
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            parsed_data = json.loads(response_text)

            # Initialize configurable fields with None values
            configurable_fields_result = {}
            for field in configurable_fields:
                configurable_fields_result[field.name] = None

            # Update with extracted values
            if "configurable_fields" in parsed_data:
                for field_name, value in parsed_data["configurable_fields"].items():
                    if field_name in configurable_fields_result:
                        configurable_fields_result[field_name] = value

            discovered_fields = parsed_data.get("discovered_fields", {})
            confidence_score = parsed_data.get("confidence_score")
            processing_notes = parsed_data.get("processing_notes")

            return ParsedDocument(
                configurable_fields=configurable_fields_result,
                discovered_fields=discovered_fields,
                confidence_score=confidence_score,
                processing_notes=processing_notes
            )

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to process LLM response: {str(e)}")
