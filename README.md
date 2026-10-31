# TanyaDok

Asisten tanya-jawab dokumen PDF berbahasa Indonesia berbasis RAG (Retrieval-Augmented Generation).
Upload PDF, ajukan pertanyaan, dapatkan jawaban beserta halaman sumbernya.

> Tambahkan screenshot atau GIF demo di sini. Ini bagian yang paling pertama dilihat orang.

## Masalah yang diselesaikan
Dokumen panduan (akademik, peraturan, SOP) itu panjang dan sulit dicari. TanyaDok mencari bagian
yang relevan dengan makna, bukan sekadar kata kunci, lalu menunjukkan halaman asalnya
supaya jawabannya bisa dicek.

## Cara kerja
1. PDF dibaca per halaman, lalu dipotong menjadi potongan ~700 karakter (tumpang tindih 120).
2. Tiap potongan diubah menjadi vektor dengan model multibahasa `multilingual-e5-small`.
3. Pertanyaan diubah menjadi vektor, lalu dicari potongan dengan cosine similarity tertinggi.
4. (Opsional) LLM merangkum jawaban hanya dari potongan tersebut dan menyebut rujukan halaman.

## Cara pakai
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Mode LLM (opsional): set `ANTHROPIC_API_KEY` di environment. Tanpa itu, aplikasi tetap jalan
dalam mode offline dan menampilkan potongan paling relevan.

## Evaluasi
```bash
python eval.py data/panduan.pdf eval/questions.json
```
| Metrik | Hasil |
|---|---|
| Jumlah soal | isi |
| Hit@4 | isi |
| MRR | isi |

## Keterbatasan
- PDF hasil scan (gambar) belum didukung, butuh OCR.
- Pemotongan teks masih berbasis jumlah karakter, belum berbasis struktur (bab/subbab).

## Rencana pengembangan
- Perbandingan ukuran potongan dan model embedding (ablation).
- Reranking dengan cross-encoder.
- Dukungan OCR untuk PDF scan.

## Penulis
Ahmad Rizky Febrian, mahasiswa AI & Robotics, Universitas Prasetiya Mulya.
