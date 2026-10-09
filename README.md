# UTS Lab Pemrograman - CRUD Data Mahasiswa

Aplikasi sederhana untuk mengelola data mahasiswa (Create, Read, Update, Delete)
dengan backend Python + Flask dan database SQLite.

## Cara menjalankan

```
pip install -r requirements.txt
python app.py
```

Lalu buka http://127.0.0.1:5000/mahasiswa

## Struktur

- `app.py` - titik masuk aplikasi, mendaftarkan blueprint dan membuat tabel
- `models/mahasiswa_model.py` - koneksi dan query SQLite
- `controllers/mahasiswa_controller.py` - route, validasi, dan perhitungan Lama Studi
- `templates/` - halaman daftar, detail, dan form tambah/edit

## Fitur

- Tambah, lihat daftar dan detail, ubah, dan hapus mahasiswa
- Validasi: NIM/nama/program studi/angkatan wajib diisi, IPK harus 0.00-4.00
- NIM yang sudah terdaftar ditolak
- Lama Studi = tahun sekarang - angkatan (dihitung program)
- Data tersimpan di `database.db` sehingga tetap ada setelah aplikasi dimatikan
