from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os


LOGO_PATH = "/mnt/data/10 - 3 x 2 - .01.png"


def _add_watermark(canvas_obj, doc):
    """
    Draws a light watermark logo at the center of the page.
    """
    if not os.path.exists(LOGO_PATH):
        return

    width, height = A4
    canvas_obj.saveState()
    canvas_obj.translate(width / 2, height / 2)
    canvas_obj.setFillAlpha(0.08)  # very light watermark
    canvas_obj.drawImage(
        LOGO_PATH,
        -2 * inch,
        -2 * inch,
        width=4 * inch,
        height=4 * inch,
        mask="auto",
    )
    canvas_obj.restoreState()


def generate_invoice_pdf(invoice, snapshot, project, file_path: str):
    """
    Generates a branded, client-ready invoice PDF.
    """
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    # --------------------------------------------------
    # HEADER LOGO
    # --------------------------------------------------
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=2.2 * inch, height=1.2 * inch)
        elements.append(logo)

    elements.append(Spacer(1, 16))

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------
    elements.append(Paragraph(
        "<b>INVOICE</b>",
        styles["Title"]
    ))

    elements.append(Spacer(1, 14))

    # --------------------------------------------------
    # INVOICE DETAILS
    # --------------------------------------------------
    elements.append(Paragraph(f"<b>Invoice ID:</b> {invoice.id}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Project ID:</b> {project.id}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Milestone:</b> {invoice.milestone.replace('_', ' ').title()}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Percentage:</b> {invoice.percentage}%", styles["Normal"]))
    elements.append(Paragraph(f"<b>Amount Payable:</b> ₹{invoice.amount}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Status:</b> {invoice.status.upper()}", styles["Normal"]))

    elements.append(Spacer(1, 18))

    # --------------------------------------------------
    # FOOTER NOTE
    # --------------------------------------------------
    elements.append(Paragraph(
        "This is a system-generated invoice issued by <b>Architectique Interiors</b> "
        "based on an approved quotation. This document is valid without signature.",
        styles["Italic"]
    ))

    # --------------------------------------------------
    # BUILD DOCUMENT WITH WATERMARK
    # --------------------------------------------------
    doc.build(
        elements,
        onFirstPage=_add_watermark,
        onLaterPages=_add_watermark
    )
