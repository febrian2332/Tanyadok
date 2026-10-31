"""Antarmuka web. Jalankan: streamlit run app.py"""
import tempfile
from pathlib import Path

import streamlit as st

from src.answer import answer
from src.rag import DocumentIndex

st.set_page_config(page_title="TanyaDok", page_icon="📄")
st.title("TanyaDok")
st.caption("Tanya jawab dokumen PDF berbahasa Indonesia, lengkap dengan sumber halaman.")

files = st.file_uploader("Upload satu atau lebih PDF", type="pdf", accept_multiple_files=True)

if files:
    key = tuple((f.name, f.size) for f in files)
    if st.session_state.get("key") != key:
        with st.spinner("Membaca dan mengindeks dokumen..."):
            tmp = Path(tempfile.mkdtemp())
            paths = []
            for f in files:
                p = tmp / f.name
                p.write_bytes(f.getvalue())
                paths.append(p)
            idx = DocumentIndex()
            idx.build(paths)
            st.session_state["idx"], st.session_state["key"] = idx, key
        st.success(f"Selesai. {len(idx.chunks)} potongan teks terindeks.")

    question = st.text_input("Pertanyaan kamu")
    if question:
        hits = st.session_state["idx"].search(question, k=4)
        st.subheader("Jawaban")
        st.write(answer(question, hits))
        st.subheader("Sumber")
        for chunk, score in hits:
            with st.expander(f"{chunk.source}, hal. {chunk.page} (skor {score:.2f})"):
                st.write(chunk.text)
