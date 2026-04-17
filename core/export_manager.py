from fpdf import FPDF
import datetime

def create_pdf_report(content, title="Study Report"):
    pdf = FPDF()
    pdf.add_page()
    
    # Font Ayarı (Türkçe karakter desteği için standart fontlar bazen yetmeyebilir)
    pdf.set_font("Helvetica", "B", 20)
    
    # Header - Lumina AI Markası
    pdf.set_text_color(99, 102, 241) # Lumina Moru
    pdf.cell(0, 10, "Lumina AI - Study Guide", ln=True, align="C")
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(128, 128, 128)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.cell(0, 10, f"Generated on: {date_str}", ln=True, align="C")
    pdf.ln(10)

    # İçerik Başlığı
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(5)

    # Ana İçerik
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    
    # Markdown'daki bazı karakterleri PDF uyumlu hale getirelim
    clean_content = content.replace("## ", "").replace("**", "").replace("- ", "• ")
    
    # Çok satırlı metin yazdırma
    pdf.multi_cell(0, 7, clean_content)
    
    # Footer
    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 10, f"Lumina AI | Intelligent Learning Assistant - Page {pdf.page_no()}", align="C")
    
    return pdf.output(dest='S') # Byte stream olarak döndür