import os

import fitz  # PyMuPDF for quick page duplication
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def create_base_styles():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=10,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
    )
    return title_style, body_style


# 1. Standard Happy Path Invoice (Equivalence Partitioning: Valid Standard Input)
def generate_valid_invoice(filename="01_valid_invoice.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    title_style, body_style = create_base_styles()

    story = [
        Paragraph("ACME ENTERPRISE SOLUTIONS", title_style),
        Paragraph("Statement ID: ACT-8849201 | Date: September 26, 2026", body_style),
        Spacer(1, 15),
    ]

    data = [
        ["Item", "Qty", "Price", "Total"],
        ["Cloud Server Subscriptions", "2", "$500.00", "$1,000.00"],
        ["AI Token Usage Allocation", "10", "$15.00", "$150.00"],
        ["Subtotal", "", "", "$1,150.00"],
    ]

    t = Table(data, colWidths=[250, 60, 80, 90])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    story.append(t)
    doc.build(story)
    print(f"Generated: {filename}")


# 2. Empty Document (Boundary Value Analysis: 0 bytes / 0 words)
def generate_empty_pdf(filename="02_empty_document.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.showPage()  # Creates a single blank page
    c.save()
    print(f"Generated: {filename}")


# 3. Corrupted / Invalid Byte Stream (Error Handling & Robustness Testing)
def generate_corrupted_pdf(filename="03_corrupted_file.pdf"):
    with open(filename, "wb") as f:
        # Invalid header and truncated binary garbage
        f.write(b"%PDF-1.7-CORRUPTED_HEADER_DATA_NOT_VALID_STRUCTURE_XYZ12345")
    print(f"Generated: {filename}")


# 4. UTF-8 & CJK Character Encoding Test (Internationalization & Font Encoding)
def generate_cjk_unicode_pdf(filename="04_unicode_cjk.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)

    # Render fallback UTF-8/CJK text via raw PyMuPDF font canvas mapping
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Multilingual & Internationalized Document")

    c.setFont("Helvetica", 10)
    c.drawString(50, 720, "English: Technical Specifications and Contract Details")
    c.drawString(50, 700, "Spanish: Especificaciones Tecnicas y Detalles del Contrato")
    c.drawString(50, 680, "French: Specifications Techniques et Details du Contrat")

    # Draw raw UTF-8 octets/text markers for parser extraction tests
    c.drawString(50, 640, "CJK Characters (Chinese / Japanese / Korean Test Payload):")
    c.drawString(50, 620, "Chinese (Simplified): 这是一个测试文档。用于验证系统解析能力。")
    c.drawString(50, 600, "Japanese: これはテスト文書です。解析機能を検証します。")
    c.drawString(50, 580, "Special Characters & Symbols: $ & @ % # * ++ == != <= >= € £ ¥")

    c.save()
    print(f"Generated: {filename}")


# 5. Massive Multi-Page Stress Document (Stress & Performance Testing)
def generate_large_multipage_pdf(filename="05_stress_multipage.pdf"):
    base_single_page = "temp_single.pdf"
    doc = SimpleDocTemplate(base_single_page, pagesize=letter)
    title_style, body_style = create_base_styles()

    story = [Paragraph("PERFORMANCE STRESS TEST PAYLOAD", title_style), Spacer(1, 10)]

    for i in range(25):
        story.append(
            Paragraph(
                f"Line item entry #{i + 1}: Automated Playwright load verification parameter. "
                "Testing memory allocation limits, string concatenation bounds, and rendering "
                "speeds.",
                body_style,
            )
        )
        story.append(Spacer(1, 4))

    doc.build(story)

    # Merge pages into a 20-page document using PyMuPDF
    src = fitz.open(base_single_page)
    dest = fitz.open()
    for _ in range(20):
        dest.insert_pdf(src)

    dest.save(filename)
    src.close()
    dest.close()
    if os.path.exists(base_single_page):
        os.remove(base_single_page)
    print(f"Generated: {filename}")


# 6. Special Formatting & Keyword Density (Combinatorial / Search Testing)
def generate_keyword_density_pdf(filename="06_keyword_density.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    title_style, body_style = create_base_styles()

    story = [
        Paragraph("SECURITY AUDIT & COMPLIANCE LOG", title_style),
        Paragraph("Target Flag: CONFIDENTIAL", body_style),
        Spacer(1, 15),
    ]

    paragraph_text = (
        "This CONFIDENTIAL report contains proprietary system secrets. "
        "Any unauthorized distribution of this CONFIDENTIAL payload will violate "
        "internal compliance policies. Mark this file as CONFIDENTIAL immediately. "
        "Search match counters should register exact instances of the key term CONFIDENTIAL."
    )

    for _ in range(5):
        story.append(Paragraph(paragraph_text, body_style))
        story.append(Spacer(1, 10))

    doc.build(story)
    print(f"Generated: {filename}")


if __name__ == "__main__":
    print("Generating Playwright PDF Test Suite Suite...\n")
    generate_valid_invoice()
    generate_empty_pdf()
    generate_corrupted_pdf()
    generate_cjk_unicode_pdf()
    generate_large_multipage_pdf()
    generate_keyword_density_pdf()
    print("\nAll 6 test PDFs generated successfully!")
