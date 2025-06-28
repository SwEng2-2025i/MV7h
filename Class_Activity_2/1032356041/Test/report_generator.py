
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
from datetime import datetime

def get_next_report_number(report_type):
    """Get the next sequential report number"""
    reports_dir = f"reports/{report_type}"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    existing_files = [f for f in os.listdir(reports_dir) if f.startswith('report_') and f.endswith('.pdf')]
    if not existing_files:
        return 1
    
    numbers = []
    for filename in existing_files:
        try:
            num = int(filename.replace('report_', '').replace('.pdf', ''))
            numbers.append(num)
        except ValueError:
            continue
    
    return max(numbers) + 1 if numbers else 1

def create_pdf_report(test_results, report_type="backend"):
    """Create a PDF report with test results"""
    report_num = get_next_report_number(report_type)
    reports_dir = f"reports/{report_type}"
    filename = f"{reports_dir}/report_{report_num:03d}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph(f"Test Report #{report_num} - {report_type.title()}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Timestamp
    timestamp = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(timestamp)
    story.append(Spacer(1, 12))
    
    # Test results
    for result in test_results:
        result_text = Paragraph(f"• {result}", styles['Normal'])
        story.append(result_text)
        story.append(Spacer(1, 6))
    
    
    doc.build(story)
    print(f"✅ PDF report generated: {filename}")
    return filename
