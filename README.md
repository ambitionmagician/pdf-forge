# PdfForge

by Dr. Brent Allen Jensen

Merge, split, and rotate PDFs from the command line — no uploads, no
websites, no accounts. Your documents never leave your machine.

## Quickstart

```bash
pip install -r requirements.txt        # just `pypdf`

python3 pdf_forge.py merge a.pdf b.pdf c.pdf -o combined.pdf
python3 pdf_forge.py split big.pdf --pages 1-3,7 -o excerpt.pdf
python3 pdf_forge.py split big.pdf --every 10 --out-dir chunks/
python3 pdf_forge.py rotate sideways.pdf --angle 90 -o fixed.pdf
python3 pdf_forge.py rotate sideways.pdf --angle 180 --pages 2 -o fixed.pdf
```

Page selections are 1-based and accept ranges and lists: `1-3,5,9-12`.

## Commands

| Command | What it does |
|---|---|
| `merge` | Concatenate two or more PDFs, in the order given |
| `split --pages` | Extract the selected pages into one PDF |
| `split --every N` | Write one PDF per N-page chunk into `--out-dir` |
| `rotate` | Rotate all pages (or `--pages` selection) by 90/180/270 degrees |

## Requirements

- Python 3.10+, `pypdf`

## Notes

- PdfForge works on the page level: it does not decrypt password-protected
  files, edit text, or OCR scans. A scanned PDF stays a scanned PDF — just
  merged, split, or turned the right way up.
- Rotation is written into the page definitions, so every reader honors it.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
