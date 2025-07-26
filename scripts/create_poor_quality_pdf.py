#!/usr/bin/env python3
"""
Create a poor quality PDF to test confidence scoring
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def create_poor_quality_pdf(filename="test_files/poor_quality_document.pdf"):
    """Create a document with poor formatting and unclear information"""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Deliberately unclear and poorly formatted content
    content = """

    unclear document with missing info

    some kind of bill maybe?

    from: somecompany
    to: somebody else

    items:
    thing1 $$$
    thing2 ???
    other stuff 100 or 200 maybe

    total: unclear amount

    contact info might be:
    phone: could be 555-1234 or 555-4321
    email: maybe@somewhere.com

    date: sometime in 2024?

    payment due: soon

    notes:
    this document has poor formatting
    missing information
    ambiguous values
    unclear structure

    """

    story.append(Paragraph(content, styles['Normal']))

    doc.build(story)
    print(f"✅ Created poor quality document: {filename}")


if __name__ == "__main__":
    os.makedirs("test_files", exist_ok=True)
    create_poor_quality_pdf()
