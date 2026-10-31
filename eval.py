import json
import sys
from pathlib import Path

from src.rag import DocumentIndex


def main(pdf: str, questions_file: str, k: int = 4) -> None:
    idx = DocumentIndex()
    idx.build([Path(pdf)])
    items = json.loads(Path(questions_file).read_text(encoding="utf-8"))

    hits, rr = 0, 0.0
    for it in items:
        results = idx.search(it["question"], k=k)
        pages = [c.page for c, _ in results]
        if it["page"] in pages:
            hits += 1
            rr += 1 / (pages.index(it["page"]) + 1)
        else:
            print(f"MELESET: {it['question']} (benar: hal. {it['page']}, dapat: {pages})")

    n = len(items)
    print(f"\nJumlah soal : {n}")
    print(f"Hit@{k}      : {hits / n:.0%}")
    print(f"MRR         : {rr / n:.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
