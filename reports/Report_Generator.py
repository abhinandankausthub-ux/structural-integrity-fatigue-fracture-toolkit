from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def generate_report(material_name, analyses):

    styles = getSampleStyleSheet()

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    elements = []

    # Title
    elements.append(Paragraph("Structural Integrity Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Material info
    elements.append(Paragraph(f"<b>Material:</b> {material_name}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Analyses section
    elements.append(Paragraph("Included Analyses", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    for a in analyses:
        elements.append(Paragraph(f"• {a}", styles["Normal"]))
        elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 20))

    # Table summary
    table_data = [["Analysis Type", "Status"]]

    for a in analyses:
        table_data.append([a, "Completed"])

    table = Table(table_data)

    elements.append(Paragraph("Analysis Summary", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Report generated using the Structural Integrity Toolkit.",
            styles["Italic"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer
