from fpdf import FPDF
import datetime

def create_pdf_report(content, title="Study Report"):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 20)
    
    pdf.set_text_color(99, 102, 241) # Lumina Moru
    pdf.cell(0, 10, "Lumina AI - Study Guide", ln=True, align="C")
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(128, 128, 128)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.cell(0, 10, f"Generated on: {date_str}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    
    clean_content = content.replace("## ", "").replace("**", "").replace("- ", "• ")
    
    pdf.multi_cell(0, 7, clean_content)
    
    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 10, f"Lumina AI | Intelligent Learning Assistant - Page {pdf.page_no()}", align="C")
    
    return pdf.output(dest='S') 