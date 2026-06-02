import io
from typing import Optional

import pdfplumber
import PyPDF2

from app.utils.logger import get_logger

logger = get_logger(__name__)


def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF using pdfplumber with PyPDF2 fallback."""
    text = _parse_with_pdfplumber(file_bytes)
    if text.strip():
        return text

    logger.warning("pdfplumber returned empty text, trying PyPDF2 fallback")
    text = _parse_with_pypdf2(file_bytes)
    if text.strip():
        return text

    logger.warning("PyPDF2 also returned empty text, attempting OCR")
    return _parse_with_ocr(file_bytes)


def _parse_with_pdfplumber(file_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)
    except Exception as exc:
        logger.error("pdfplumber parsing failed: %s", exc)
        return ""


def _parse_with_pypdf2(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages = [reader.pages[i].extract_text() or "" for i in range(len(reader.pages))]
        return "\n".join(pages)
    except Exception as exc:
        logger.error("PyPDF2 parsing failed: %s", exc)
        return ""


def _parse_with_ocr(file_bytes: bytes) -> str:
    """Attempt OCR using pytesseract for scanned PDFs."""
    try:
        import pytesseract
        from PIL import Image

        try:
            from pdf2image import convert_from_bytes  # optional dependency

            images = convert_from_bytes(file_bytes, first_page=1, last_page=3)
            texts = [pytesseract.image_to_string(img) for img in images]
            return "\n".join(texts)
        except ImportError:
            logger.warning("pdf2image not available; OCR skipped")
            return ""
    except ImportError:
        logger.warning("pytesseract not available; OCR skipped")
        return ""
    except Exception as exc:
        logger.error("OCR failed: %s", exc)
        return ""


def parse_txt(file_bytes: bytes) -> str:
    """Decode a plain-text file with UTF-8 fallback to latin-1."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="replace")


def parse_document(file_bytes: bytes, filename: str) -> Optional[str]:
    """Dispatch parsing based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        text = parse_pdf(file_bytes)
    elif lower.endswith(".txt"):
        text = parse_txt(file_bytes)
    else:
        logger.error("Unsupported file type: %s", filename)
        return None

    if not text.strip():
        logger.warning("Parsed document is empty: %s", filename)
        return None

    return text
