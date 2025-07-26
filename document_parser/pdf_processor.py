import PyPDF2
import io
from typing import Optional, List
import base64
from pdf2image import convert_from_bytes
from PIL import Image


class PDFProcessor:
    """Handles PDF file processing and text extraction"""

    @staticmethod
    def extract_text_from_pdf(pdf_content: bytes) -> str:
        """
        Extract text content from PDF bytes

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Extracted text as string

        Raises:
            Exception: If PDF processing fails
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"

            # Clean up the text
            text = text.strip()
            if not text:
                raise Exception("No text could be extracted from the PDF")

            return text

        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def validate_pdf(pdf_content: bytes) -> bool:
        """
        Validate if the content is a valid PDF

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            PyPDF2.PdfReader(pdf_file)
            return True
        except:
            return False

    @staticmethod
    def convert_pdf_to_images(pdf_content: bytes) -> List[str]:
        """
        Convert PDF pages to base64-encoded images for vision API

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            List of base64-encoded PNG images (one per page)

        Raises:
            Exception: If PDF to image conversion fails
        """
        try:
            # Convert PDF to images (200 DPI for good quality)
            images = convert_from_bytes(pdf_content, dpi=200, fmt='PNG')

            base64_images = []
            for image in images:
                # Convert PIL Image to base64
                buffer = io.BytesIO()
                image.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                base64_images.append(img_str)

            return base64_images
        except Exception as e:
            raise Exception(f"Failed to convert PDF to images: {str(e)}")
