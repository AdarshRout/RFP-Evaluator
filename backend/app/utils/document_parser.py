import io
from pypdf import PdfReader
from docx import Document


def parse_bytes(content: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return _from_pdf(content)
    if ext == "docx":
        return _from_docx(content)
    return content.decode("utf-8", errors="replace")


def _from_pdf(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    return "\n\n".join(p.extract_text() for p in reader.pages if p.extract_text())


def _from_docx(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
