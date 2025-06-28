import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def next_report_filename(folder="reports"):
    os.makedirs(folder, exist_ok=True)
    existing = sorted(f for f in os.listdir(folder) if f.endswith(".pdf"))
    number = len(existing) + 1
    return os.path.join(folder, f"reporte_{number:03}.pdf")

def save_report(text_lines, filename=None):
    if not filename:
        filename = next_report_filename()
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text_lines:
        c.drawString(40, y, line)
        y -= 20
    c.save()
    print(f"Reporte generado: {filename}")
