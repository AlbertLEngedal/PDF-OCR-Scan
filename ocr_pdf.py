#!/usr/bin/env python3
"""Simple CLI for running OCR on PDF files to produce searchable PDFs."""

from __future__ import annotations

import argparse
import io
import logging
from pathlib import Path

from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfMerger


def ocr_pdf(input_pdf: Path, output_pdf: Path, dpi: int) -> None:
    """Run OCR on *input_pdf* and write a searchable PDF to *output_pdf*."""
    logging.info("Converting %s to images at %s DPI", input_pdf, dpi)
    images = convert_from_path(str(input_pdf), dpi=dpi)

    if not images:
        raise ValueError(f"No pages were found in {input_pdf}")

    merger = PdfMerger()
    try:
        for page_number, image in enumerate(images, start=1):
            logging.info("Performing OCR on page %s", page_number)
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension="pdf")
            merger.append(io.BytesIO(pdf_bytes))

        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        with output_pdf.open("wb") as fh:
            merger.write(fh)
        logging.info("Wrote searchable PDF to %s", output_pdf)
    finally:
        merger.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_pdf", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to the output searchable PDF (defaults to '<input>_searchable.pdf')",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution to use when rasterizing the PDF (default: 300 DPI)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    input_pdf: Path = args.input_pdf
    output_pdf: Path = args.output or input_pdf.with_name(f"{input_pdf.stem}_searchable.pdf")

    if not input_pdf.is_file():
        raise FileNotFoundError(f"Input PDF '{input_pdf}' does not exist")

    ocr_pdf(input_pdf.resolve(), output_pdf.resolve(), args.dpi)


if __name__ == "__main__":
    main()
