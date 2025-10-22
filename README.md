# PDF OCR Scan

A simple utility for converting PDFs into searchable PDFs using Tesseract OCR.

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This script requires a Tesseract installation that is accessible on your `PATH`.
`pdf2image` also depends on [Poppler](https://poppler.freedesktop.org/).

On Ubuntu/Debian:

```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

On macOS (with Homebrew):

```bash
brew install tesseract
brew install poppler
```

## Usage

```bash
python ocr_pdf.py input.pdf [-o output.pdf] [--dpi 300] [-v]
```

* `input.pdf` – Path to the PDF you want to OCR.
* `-o/--output` – Optional path for the searchable PDF (defaults to `<input>_searchable.pdf`).
* `--dpi` – Rasterization resolution (defaults to 300).
* `-v/--verbose` – Enable detailed logging output.

## How it works

1. Each page of the source PDF is rasterized into an image.
2. `pytesseract` runs OCR on each image and generates a searchable PDF page.
3. The per-page PDFs are merged into the final searchable document.

## Notes

* High-resolution scans (>=300 DPI) usually yield better OCR results.
* Deskewing or cleaning the images before OCR can improve accuracy for poor quality scans.

## Committing your changes

If you make adjustments to the script or documentation, you can commit them with Git:

```bash
git status               # inspect the files you changed
git add <path> [...]     # stage the updates you want to keep
git commit -m "Describe the change"
```

Replace `<path>` with the files you modified and tailor the commit message so it summarizes the update clearly. After committing, you can continue iterating or push the commit to your own fork or remote as needed.
