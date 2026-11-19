"""Download original research PDFs into a local archive."""
import argparse
import json
import shutil
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--redistributable-only", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(__file__).with_name("catalog.json")
    papers = json.loads(manifest_path.read_text(encoding="utf-8"))
    args.destination.mkdir(parents=True, exist_ok=True)
    failures = 0
    for paper in papers:
        if args.redistributable_only and not paper.get("license"):
            continue
        if paper["access"] != "direct-pdf":
            print(f"Manual download: {paper['filename']} — {paper['url']}")
            continue
        path = args.destination / paper["filename"]
        if path.exists():
            with path.open("rb") as existing:
                if existing.read(5) == b"%PDF-":
                    print(f"Already present: {path.name}")
                    continue
            print(f"Invalid existing file, left untouched: {path}")
            failures += 1
            continue
        try:
            request = Request(paper["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=45) as response, tempfile.TemporaryFile() as pdf:
                header = response.read(5)
                if header != b"%PDF-":
                    raise ValueError("server did not return a PDF")
                pdf.write(header)
                shutil.copyfileobj(response, pdf)
                pdf.seek(0)
                with path.open("xb") as output:
                    try:
                        shutil.copyfileobj(pdf, output)
                    except OSError:
                        path.unlink()
                        raise
            print(f"Saved: {path.name}")
        except (OSError, ValueError) as error:
            failures += 1
            print(f"Download failed: {path.name} — {error}")
    return int(failures > 0)

if __name__ == "__main__":
    raise SystemExit(main())
