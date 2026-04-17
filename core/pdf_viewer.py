import fitz
from typing import Optional, List


def render_page(
    pdf_bytes: bytes,
    page_num: int,
    highlight_texts: Optional[List[str]] = None,
    dpi: int = 150,
) -> bytes:
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    total = len(pdf)
    page_num = max(1, min(page_num, total))
    page = pdf[page_num - 1]

    if highlight_texts:
        for raw_text in highlight_texts:
            text = raw_text.strip()
            if not text:
                continue
            found = _search(page, text)
            for rect in found:
                ann = page.add_highlight_annot(rect)
                ann.set_colors(stroke=(1.0, 0.92, 0.23))
                ann.update()

    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img_bytes = pix.tobytes("png")
    pdf.close()
    return img_bytes


def _search(page, text: str) -> list:
    candidates = [
        text[:120],
        text[:80],
        " ".join(text.split()[:10]),
        " ".join(text.split()[:6]),
    ]
    for query in candidates:
        query = query.strip()
        if len(query) < 4:
            continue
        results = page.search_for(query, quads=False)
        if results:
            return results
    return []


def get_total_pages(pdf_bytes: bytes) -> int:
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    n = len(pdf)
    pdf.close()
    return n
