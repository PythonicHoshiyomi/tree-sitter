# Cek - CLI Pemeriksa Kode Python Berbasis Tree-sitter

Tool CLI sederhana berbasis `tree-sitter` untuk memeriksa basis kode Python.

## Fitur
1. **Pendeteksi TODO / FIXME**: Menemukan komentar yang mengandung `TODO` atau `FIXME` beserta nomor barisnya menggunakan query Tree-sitter dan predikat `#match?`.
2. **Pendeteksi Fungsi Panjang**: Melaporkan fungsi yang memiliki panjang lebih dari 30 baris (termasuk fungsi di dalam kelas atau fungsi bersarang).
3. **Pendeteksi Error Sintaks**: Mendeteksi file yang pohon sintaksnya mengandung node error/missing (`root_node.has_error`) serta menunjukkan baris pertama tempat terjadinya error.

## Instalasi Dependensi
Pastikan Python 3.10+ sudah terpasang, lalu instal paket berikut:
```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan
Jalankan skrip `cek.py` dengan memberikan path folder yang ingin diperiksa:
```bash
python cek.py <path_folder>
```

Contoh menjalankan pada folder uji:
```bash
python cek.py uji
```

## Contoh Output
```text
[TODO/FIXME] uji\f1_todo.py:2: # TODO: implementasikan validasi input
[TODO/FIXME] uji\f1_todo.py:4: # FIXME: perbaiki penanganan error
[FUNGSI PANJANG] uji\f2_panjang.py:1: fungsi 'fungsi_sangat_panjang' (33 baris)
[ERROR SINTAKS] uji\f3_error.py:1: file mengandung kesalahan sintaks
```

## Catatan
- Folder sistem/dependensi seperti `.git`, `.venv`, `venv`, dan `node_modules` secara otomatis dilewati saat pemindaian.
- Semua fungsi yang terdefinisi (termasuk method kelas) dihitung jumlah barisnya dari `start_point` hingga `end_point`.
