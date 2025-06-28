
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_reporte(nombre_reporte, resultados):
    carpeta = os.path.join(os.path.dirname(__file__), 'Generated')
    os.makedirs(carpeta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(carpeta, f"{nombre_reporte}_reporte_{timestamp}.pdf")

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, f"Reporte de {nombre_reporte}")

    c.setFont("Helvetica", 12)
    y = height - 100
    for linea in resultados:
        c.drawString(72, y, linea)
        y -= 20
        if y < 72:
            c.showPage()
            y = height - 72

    c.save()
    print(f"Reporte generado: {filename}")
