"""Inti TanyaDok: baca PDF -> potong -> embedding -> cari paling relevan."""
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Model multibahasa kecil, mendukung bahasa Indonesia, jalan di CPU.
MODEL_NAME = "intfloat/multilingual-e5-small"


@dataclass
class Chunk:
    text: str
    source: str  # nama file
    page: int    # nomor halaman (mulai dari 1)


def split_text(text: str, size: int = 700, overlap: int = 120) -> list[str]:
    """Potong teks jadi potongan ~size karakter dengan tumpang tindih."""
    text = re.sub(r"\s+", " ", text).strip()
    step = max(size - overlap, 1)
    return [text[i:i + size] for i in range(0, len(text), step) if text[i:i + size]]


def read_pdf(path: Path) -> list[Chunk]:
    chunks = []
    reader = PdfReader(str(path))
    for page_no, page in enumerate(reader.pages, start=1):
        for piece in split_text(page.extract_text() or ""):
            chunks.append(Chunk(piece, path.name, page_no))
    return chunks


class DocumentIndex:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks: list[Chunk] = []
        self.vectors: np.ndarray | None = None

    def build(self, pdf_paths: list[Path]) -> None:
        self.chunks = [c for p in pdf_paths for c in read_pdf(Path(p))]
        if not self.chunks:
            raise ValueError("Tidak ada teks yang terbaca. PDF hasil scan butuh OCR dulu.")
        # E5 butuh awalan "passage: " untuk dokumen dan "query: " untuk pertanyaan.
        texts = [f"passage: {c.text}" for c in self.chunks]
        self.vectors = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        q = self.model.encode([f"query: {query}"], normalize_embeddings=True)[0]
        scores = self.vectors @ q  # cosine similarity (vektor sudah dinormalisasi)
        top = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top]

    def save(self, folder: str = "index") -> None:
        Path(folder).mkdir(exist_ok=True)
        np.save(Path(folder) / "vectors.npy", self.vectors)
        (Path(folder) / "chunks.json").write_text(
            json.dumps([asdict(c) for c in self.chunks], ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, folder: str = "index") -> "DocumentIndex":
        idx = cls()
        idx.vectors = np.load(Path(folder) / "vectors.npy")
        raw = json.loads((Path(folder) / "chunks.json").read_text(encoding="utf-8"))
        idx.chunks = [Chunk(**r) for r in raw]
        return idx
