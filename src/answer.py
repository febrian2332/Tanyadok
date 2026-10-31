"""Membuat jawaban dari potongan dokumen. Ada dua mode:
1. Ekstraktif (default, offline): tampilkan potongan paling relevan.
2. LLM (opsional): kalau ANTHROPIC_API_KEY terisi, jawaban dirangkum LLM
   hanya dari konteks yang ditemukan, lengkap dengan rujukan halaman.
"""
import os

from .rag import Chunk

LLM_MODEL = os.getenv("TANYADOK_MODEL", "claude-sonnet-5-5")


def _context(hits: list[tuple[Chunk, float]]) -> str:
    return "\n\n".join(f"[{c.source}, hal. {c.page}]\n{c.text}" for c, _ in hits)


def answer(question: str, hits: list[tuple[Chunk, float]]) -> str:
    if not os.getenv("ANTHROPIC_API_KEY"):
        best, _ = hits[0]
        return f"(Mode offline) Potongan paling relevan ada di {best.source}, hal. {best.page}:\n\n{best.text}"

    import anthropic
    client = anthropic.Anthropic()
    prompt = (
        "Jawab pertanyaan dalam bahasa Indonesia HANYA berdasarkan konteks di bawah. "
        "Sebutkan rujukan dengan format (nama file, hal. X). "
        "Jika jawaban tidak ada di konteks, katakan tidak ditemukan.\n\n"
        f"KONTEKS:\n{_context(hits)}\n\nPERTANYAAN: {question}"
    )
    msg = client.messages.create(
        model=LLM_MODEL, max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
