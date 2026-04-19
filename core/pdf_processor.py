import fitz  # PyMuPDF
import tempfile
import os
import io
import csv
from docx import Document as DocxDocument
from pptx import Presentation
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

try:
    import pytesseract
    from PIL import Image

    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path 

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def load_pdf(file_bytes: bytes, filename: str) -> List[Document]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    documents = []
    try:
        pdf = fitz.open(tmp_path)
        total_pages = len(pdf)
        for page_num in range(total_pages):
            page = pdf[page_num]
            text = page.get_text("text")
            
            if len(text.strip()) < 50 and OCR_AVAILABLE:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Çözünürlüğü artır
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img, lang="tur+eng")

            if text.strip():
                documents.append(Document(
                    page_content=text,
                    metadata={"page": page_num + 1, "total_pages": total_pages, "source": filename}
                ))
        pdf.close()
    finally:
        os.unlink(tmp_path)
    return documents

def load_docx(file_bytes: bytes, filename: str) -> List[Document]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        doc = DocxDocument(tmp_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return [Document(page_content=text, metadata={"page": 1, "total_pages": 1, "source": filename})]
    finally:
        os.unlink(tmp_path)

def load_pptx(file_bytes: bytes, filename: str) -> List[Document]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        prs = Presentation(tmp_path)
        text = []
        for i, slide in enumerate(prs.slides):
            slide_text = f"--- Slide {i+1} ---\n"
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text += shape.text + "\n"
            text.append(slide_text)
        full_text = "\n".join(text)
        return [Document(page_content=full_text, metadata={"page": 1, "total_pages": len(prs.slides), "source": filename})]
    finally:
        os.unlink(tmp_path)

def load_csv(file_bytes: bytes, filename: str) -> List[Document]:
    text = file_bytes.decode("utf-8", errors="replace")
    return [Document(page_content=text, metadata={"page": 1, "total_pages": 1, "source": filename})]

def load_txt(file_bytes: bytes, filename: str) -> List[Document]:
    text = file_bytes.decode("utf-8", errors="replace")
    return [Document(page_content=text, metadata={"page": 1, "total_pages": 1, "source": filename})]

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)
    return splitter.split_documents(documents)

def load_and_split(file_bytes: bytes, filename: str) -> List[Document]:
    ext = filename.lower().split('.')[-1]
    
    if ext == "pdf":
        raw_docs = load_pdf(file_bytes, filename)
    elif ext == "docx":
        raw_docs = load_docx(file_bytes, filename)
    elif ext == "pptx":
        raw_docs = load_pptx(file_bytes, filename)
    elif ext == "csv":
        raw_docs = load_csv(file_bytes, filename)
    else:
        raw_docs = load_txt(file_bytes, filename)
        
    return split_documents(raw_docs)