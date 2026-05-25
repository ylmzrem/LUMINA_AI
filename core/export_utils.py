from fpdf import FPDF
import datetime

class LuminaPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(99, 102, 241)
        self.cell(0, 10, "Lumina AI Study Report", ln=True, align="C")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def clean_text_for_pdf(text):
    """Replaces Turkish and special characters with PDF-safe equivalents."""
    if not isinstance(text, str):
        return text
        
    replacements = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S',
        'ğ': 'g', 'Ğ': 'G', 'ç': 'c', 'Ç': 'C',
        'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U',
        '”': '"', '“': '"', '’': "'", '‘': "'", '–': '-'
    }
    
    safe_text = text
    for tr_char, en_char in replacements.items():
        safe_text = safe_text.replace(tr_char, en_char)
        
    return safe_text

def export_to_pdf(content, title):
    pdf = LuminaPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 14)
    safe_title = clean_text_for_pdf(title)
    pdf.cell(0, 10, safe_title, ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 11)
    
    clean_text = content.replace("## ", "")
    clean_text = clean_text.replace("**", "")
    clean_text = clean_text.replace("*", "-")
    clean_text = clean_text.replace("[", "- ").replace("]", "")
    clean_text = clean_text.replace("“", '"').replace("”", '"')
    clean_text = clean_text.replace("‘", "'").replace("’", "'")
    
    clean_text = clean_text_for_pdf(clean_text)
    
    pdf.multi_cell(0, 8, clean_text)
    return pdf.output(dest='S')