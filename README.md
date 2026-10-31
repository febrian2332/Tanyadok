# TanyaDok

Asisten tanya-jawab dokumen PDF berbahasa Indonesia berbasis RAG (Retrieval-Augmented Generation).
Upload PDF, ajukan pertanyaan, dapatkan bagian dokumen yang paling relevan beserta halaman sumbernya.

![Demo TanyaDok](demo.png)

## Masalah yang diselesaikan
Dokumen panjang (modul kuliah, panduan, peraturan) sulit dicari dengan pencarian kata kunci biasa.
TanyaDok mencari berdasarkan makna, lalu menunjukkan halaman asalnya supaya hasilnya bisa dicek.

## Cara kerja
1. PDF dibaca per halaman, lalu dipotong menjadi potongan ~700 karakter (tumpang tindih 120).
2. Tiap potongan diubah menjadi vektor dengan model multibahasa `intfloat/multilingual-e5-small`.
3. Pertanyaan diubah menjadi vektor, lalu dicari 4 potongan dengan cosine similarity tertinggi.
4. Jika skor tertinggi di bawah ambang (0,78), aplikasi menyatakan tidak ada bagian yang relevan.
5. (Opsional) Jika `ANTHROPIC_API_KEY` diisi, LLM merangkum jawaban hanya dari potongan yang ditemukan.

## Cara pakai
```bash
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Pertama kali dijalankan, model embedding (~470 MB) diunduh otomatis. Tanpa API key, aplikasi berjalan
dalam mode offline dan menampilkan potongan teks paling relevan.

## Hasil uji awal
Diuji manual pada satu dokumen latihan sistem bilangan (konversi biner/heksadesimal, 27 potongan teks):
- Pertanyaan yang sesuai isi dokumen mendapat skor kemiripan sekitar 0,80 sampai 0,83.
- Pertanyaan di luar topik (misalnya soal presiden) tetap mendapat skor sekitar 0,76, selisihnya tipis.
  Karena itu, ambang 0,78 saat ini hanya perkiraan awal dan perlu dikalibrasi dengan evaluasi yang lebih besar.

Skrip evaluasi (`eval.py`, menghitung Hit@k dan MRR) sudah tersedia, tetapi evaluasi kuantitatif
pada kumpulan soal yang lebih besar belum dijalankan.

## Keterbatasan
- PDF hasil scan (gambar) belum didukung, butuh OCR.
- Pemotongan teks berbasis jumlah karakter, sehingga potongan bisa terhenti di tengah kalimat.
- Skor kemiripan model kecil belum cukup tegas membedakan pertanyaan relevan dan tidak relevan.
- Mode offline menampilkan teks mentah, bukan jawaban yang dirangkum.

## Rencana pengembangan
- Pemotongan teks berbasis kalimat atau struktur dokumen.
- Kalibrasi ambang relevansi dari evaluasi yang lebih besar.
- Perbandingan ukuran potongan dan model embedding.
- Reranking dengan cross-encoder dan dukungan OCR.

## Penulis
Ahmad Rizky Febrian, mahasiswa Artificial Intelligence and Robotics, Universitas Prasetiya Mulya.
