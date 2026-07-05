import logging

import pypdfium2 as pdfium

logger = logging.getLogger(__name__)


def extract_text_from_pdf(path: str) -> str:
    try:
        pdf = pdfium.PdfDocument(path)
    except Exception as exc:
        msg = str(exc).lower()
        if "encrypt" in msg or "password" in msg:
            logger.warning("Cannot open encrypted PDF without password: %s", path)
            raise ValueError("PDF is encrypted; provide a password to decrypt.") from exc
        logger.exception("Failed to open PDF: %s", path)
        raise

    pages = []
    for i in range(len(pdf)):
        page = pdf[i]
        textpage = page.get_textpage()
        pages.append(textpage.get_text_bounded())
    return "\n".join(pages)
