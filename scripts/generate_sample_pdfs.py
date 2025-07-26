#!/usr/bin/env python3
"""
Generate sample PDF documents for testing the document parser
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime, timedelta
import os


def create_sample_invoice_pdf(filename="sample_invoice.pdf"):
    """Create a sample invoice PDF for testing"""

    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue
    )

    # Title
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))

    # Company info
    company_info = """
    <b>ACME Corporation</b><br/>
    123 Business Street<br/>
    Business City, BC 12345<br/>
    Phone: (555) 123-4567<br/>
    Email: billing@acmecorp.com
    """
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Spacer(1, 20))

    # Invoice details
    invoice_date = datetime.now()
    due_date = invoice_date + timedelta(days=30)

    invoice_details = [
        ['Invoice Number:', 'INV-2024-001'],
        ['Invoice Date:', invoice_date.strftime('%Y-%m-%d')],
        ['Due Date:', due_date.strftime('%Y-%m-%d')],
        ['Customer ID:', 'CUST-12345']
    ]

    invoice_table = Table(invoice_details, colWidths=[2*inch, 2*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    story.append(invoice_table)
    story.append(Spacer(1, 30))

    # Bill to section
    story.append(Paragraph("<b>Bill To:</b>", styles['Heading3']))
    bill_to = """
    John Smith<br/>
    Tech Solutions Inc.<br/>
    456 Client Avenue<br/>
    Client City, CC 67890<br/>
    john.smith@techsolutions.com<br/>
    Phone: (555) 987-6543
    """
    story.append(Paragraph(bill_to, styles['Normal']))
    story.append(Spacer(1, 20))

    # Items table
    story.append(Paragraph("<b>Items:</b>", styles['Heading3']))

    items_data = [
        ['Description', 'Quantity', 'Unit Price', 'Total'],
        ['Web Development Services', '40 hours', '$125.00', '$5,000.00'],
        ['Database Setup', '8 hours', '$150.00', '$1,200.00'],
        ['Testing & QA', '12 hours', '$100.00', '$1,200.00'],
        ['Project Management', '5 hours', '$175.00', '$875.00']
    ]

    items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(items_table)
    story.append(Spacer(1, 20))

    # Totals
    totals_data = [
        ['Subtotal:', '$8,275.00'],
        ['Tax (8.5%):', '$703.38'],
        ['Total Amount:', '$8,978.38']
    ]

    totals_table = Table(totals_data, colWidths=[3*inch, 1*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
    ]))

    story.append(totals_table)
    story.append(Spacer(1, 30))

    # Payment terms
    story.append(Paragraph("<b>Payment Terms:</b>", styles['Heading3']))
    payment_terms = """
    Payment is due within 30 days of invoice date.<br/>
    Late payments may be subject to a 1.5% monthly service charge.<br/>
    Please reference invoice number INV-2024-001 with payment.<br/><br/>

    <b>Payment Methods:</b><br/>
    - Check payable to: ACME Corporation<br/>
    - Wire Transfer: Account #123456789, Routing #987654321<br/>
    - Online Payment: www.acmecorp.com/pay
    """
    story.append(Paragraph(payment_terms, styles['Normal']))

    # Build the PDF
    doc.build(story)
    print(f"✅ Created sample invoice: {filename}")


def create_sample_resume_pdf(filename="sample_resume.pdf"):
    """Create a sample resume PDF for testing"""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Name and title
    name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1,  # Center
        textColor=colors.darkblue
    )

    story.append(Paragraph("Sarah Johnson", name_style))
    story.append(Paragraph("Senior Software Engineer", styles['Heading2']))
    story.append(Spacer(1, 20))

    # Contact info
    contact_info = """
    <b>Contact Information:</b><br/>
    Email: sarah.johnson@email.com<br/>
    Phone: (555) 234-5678<br/>
    Address: 789 Developer Lane, Code City, CC 54321<br/>
    LinkedIn: linkedin.com/in/sarahjohnson<br/>
    GitHub: github.com/sarahjohnson
    """
    story.append(Paragraph(contact_info, styles['Normal']))
    story.append(Spacer(1, 20))

    # Professional summary
    story.append(Paragraph("<b>Professional Summary</b>", styles['Heading3']))
    summary = """
    Experienced software engineer with 8+ years of expertise in full-stack development,
    cloud architecture, and team leadership. Proven track record of delivering scalable
    solutions and mentoring junior developers. Specializes in Python, JavaScript, and AWS.
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 15))

    # Work experience
    story.append(Paragraph("<b>Work Experience</b>", styles['Heading3']))

    experience = """
    <b>Senior Software Engineer</b> | TechStart Inc. | 2020 - Present<br/>
    • Led development of microservices architecture serving 1M+ users<br/>
    • Implemented CI/CD pipelines reducing deployment time by 60%<br/>
    • Mentored 5 junior developers and conducted technical interviews<br/><br/>

    <b>Software Engineer</b> | Innovation Labs | 2018 - 2020<br/>
    • Developed RESTful APIs using Python Flask and Django<br/>
    • Built responsive web applications with React and Redux<br/>
    • Collaborated with cross-functional teams in Agile environment<br/><br/>

    <b>Junior Developer</b> | StartupCo | 2016 - 2018<br/>
    • Created automated testing suites improving code coverage to 95%<br/>
    • Participated in code reviews and technical documentation<br/>
    • Learned modern development practices and tools
    """
    story.append(Paragraph(experience, styles['Normal']))
    story.append(Spacer(1, 15))

    # Education
    story.append(Paragraph("<b>Education</b>", styles['Heading3']))
    education = """
    <b>Master of Science in Computer Science</b><br/>
    University of Technology | 2014 - 2016<br/>
    GPA: 3.8/4.0<br/><br/>

    <b>Bachelor of Science in Software Engineering</b><br/>
    State University | 2010 - 2014<br/>
    Magna Cum Laude, GPA: 3.7/4.0
    """
    story.append(Paragraph(education, styles['Normal']))
    story.append(Spacer(1, 15))

    # Skills
    story.append(Paragraph("<b>Technical Skills</b>", styles['Heading3']))
    skills = """
    <b>Programming Languages:</b> Python, JavaScript, TypeScript, Java, Go<br/>
    <b>Frameworks:</b> Django, Flask, React, Node.js, Express<br/>
    <b>Databases:</b> PostgreSQL, MongoDB, Redis<br/>
    <b>Cloud:</b> AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes<br/>
    <b>Tools:</b> Git, Jenkins, Terraform, Elasticsearch
    """
    story.append(Paragraph(skills, styles['Normal']))

    doc.build(story)
    print(f"✅ Created sample resume: {filename}")


def create_sample_contract_pdf(filename="sample_contract.pdf"):
    """Create a sample contract PDF for testing"""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1,
        textColor=colors.darkblue
    )

    story.append(Paragraph("SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 20))

    # Contract details
    contract_info = """
    <b>Contract Number:</b> SA-2024-007<br/>
    <b>Date:</b> """ + datetime.now().strftime('%B %d, %Y') + """<br/>
    <b>Effective Date:</b> """ + datetime.now().strftime('%B %d, %Y') + """<br/>
    <b>Expiration Date:</b> """ + (datetime.now() + timedelta(days=365)).strftime('%B %d, %Y') + """<br/>
    """
    story.append(Paragraph(contract_info, styles['Normal']))
    story.append(Spacer(1, 20))

    # Parties
    story.append(Paragraph("<b>PARTIES</b>", styles['Heading3']))
    parties = """
    <b>Service Provider:</b><br/>
    Digital Solutions LLC<br/>
    555 Tech Drive, Suite 200<br/>
    Innovation City, IC 98765<br/>
    Phone: (555) 111-2222<br/>
    Email: contracts@digitalsolutions.com<br/><br/>

    <b>Client:</b><br/>
    Modern Enterprises Corp.<br/>
    888 Business Plaza<br/>
    Corporate Town, CT 13579<br/>
    Phone: (555) 333-4444<br/>
    Email: procurement@modernenterprises.com
    """
    story.append(Paragraph(parties, styles['Normal']))
    story.append(Spacer(1, 15))

    # Services
    story.append(Paragraph("<b>SERVICES</b>", styles['Heading3']))
    services = """
    The Service Provider agrees to provide the following services:<br/>
    1. Custom software development and maintenance<br/>
    2. Technical consulting and system architecture<br/>
    3. 24/7 technical support and monitoring<br/>
    4. Regular security audits and updates<br/>
    5. Staff training and documentation
    """
    story.append(Paragraph(services, styles['Normal']))
    story.append(Spacer(1, 15))

    # Payment terms
    story.append(Paragraph("<b>PAYMENT TERMS</b>", styles['Heading3']))
    payment = """
    <b>Total Contract Value:</b> $150,000.00<br/>
    <b>Payment Schedule:</b><br/>
    • Initial Payment: $50,000.00 (due upon signing)<br/>
    • Monthly Payments: $8,333.33 (12 months)<br/>
    • Final Payment: $8,333.96 (month 12)<br/><br/>

    All payments are due within 15 days of invoice date.
    Late payments subject to 2% monthly penalty.
    """
    story.append(Paragraph(payment, styles['Normal']))
    story.append(Spacer(1, 15))

    # Signatures
    story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading3']))
    signatures = """
    <b>Service Provider:</b><br/>
    _________________________<br/>
    Michael Chen, CEO<br/>
    Digital Solutions LLC<br/>
    Date: _________________<br/><br/>

    <b>Client:</b><br/>
    _________________________<br/>
    Jennifer Adams, CTO<br/>
    Modern Enterprises Corp.<br/>
    Date: _________________
    """
    story.append(Paragraph(signatures, styles['Normal']))

    doc.build(story)
    print(f"✅ Created sample contract: {filename}")


if __name__ == "__main__":
    print("🔧 Generating sample PDF documents for testing...")
    print("=" * 50)

    # Create test_files directory
    os.makedirs("test_files", exist_ok=True)

    # Generate sample PDFs
    create_sample_invoice_pdf("test_files/sample_invoice.pdf")
    create_sample_resume_pdf("test_files/sample_resume.pdf")
    create_sample_contract_pdf("test_files/sample_contract.pdf")

    print("\n🎉 Sample PDF files created in 'test_files/' directory:")
    print("- sample_invoice.pdf (invoice with financial data)")
    print("- sample_resume.pdf (resume with personal/professional info)")
    print("- sample_contract.pdf (contract with legal terms)")
    print("\nYou can now test the document parser with these files!")
