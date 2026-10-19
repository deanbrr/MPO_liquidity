"""Extract text from a PDF to a .txt file, page-tagged. Usage: python -I extract_pdf.py in.pdf out.txt"""
import sys

from pypdf import PdfReader


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    reader = PdfReader(src)
    with open(dst, "w", encoding="utf-8") as fh:
        for i, page in enumerate(reader.pages, start=1):
            try:
                txt = page.extract_text() or ""
            except Exception as exc:  # noqa: BLE001
                txt = f"[extract error: {exc}]"
            fh.write(f"\n=== PAGE {i} ===\n{txt}\n")
    print(f"pages={len(reader.pages)} -> {dst}")


if __name__ == "__main__":
    main()
