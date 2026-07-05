from pathlib import Path

import pytest

from parser import extract_text_from_pdf


def _make_pdf(text: str = "Hello, World!") -> bytes:
    content = f"BT /F1 12 Tf 100 700 Td ({text}) Tj ET".encode()
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = (
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"/Contents 4 0 R\n/Resources << /Font << /F1 5 0 R >> >>\n>>\nendobj\n"
    )
    obj4 = (
        b"4 0 obj\n<< /Length " + str(len(content)).encode() + b" >>\nstream\n"
        + content + b"\nendstream\nendobj\n"
    )
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    objs = [obj1, obj2, obj3, obj4, obj5]
    header = b"%PDF-1.4\n"
    offsets = [0] * len(objs)
    offset = len(header)
    for i, obj in enumerate(objs):
        offsets[i] = offset
        offset += len(obj)
    body = b"".join(objs)
    n = len(objs) + 1
    xref_entries = [b"0000000000 65535 f \n"]
    for o in offsets:
        xref_entries.append(f"{o:010d} 00000 n \n".encode())
    xref = b"xref\n0 " + str(n).encode() + b"\n" + b"".join(xref_entries)
    trailer = b"trailer\n<< /Size " + str(n).encode() + b" /Root 1 0 R >>\n"
    eof = b"startxref\n" + str(len(header) + len(body)).encode() + b"\n%%EOF\n"
    return header + body + xref + trailer + eof


def test_extract_text_from_pdf(tmp_path: Path) -> None:
    pdf_bytes = _make_pdf("Hello World")
    p = tmp_path / "test.pdf"
    p.write_bytes(pdf_bytes)
    text = extract_text_from_pdf(str(p))
    assert "Hello World" in text


def test_extract_invalid_file(tmp_path: Path) -> None:
    p = tmp_path / "test.pdf"
    p.write_bytes(b"not a pdf")
    with pytest.raises((ValueError, Exception)):
        extract_text_from_pdf(str(p))
