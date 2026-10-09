# models/mahasiswa_model.py
# Semua urusan database (SQLite) ada di file ini.
import os
import sqlite3

# File database disimpan di folder proyek, jadi data tetap ada
# walaupun aplikasi dimatikan lalu dijalankan lagi.
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # <- supaya hasil query bisa diakses pakai nama kolom
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            nim            INTEGER PRIMARY KEY,
            nama           TEXT    NOT NULL,
            program_studi  TEXT    NOT NULL,
            angkatan       INTEGER NOT NULL,
            ipk            REAL    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# READ ALL
def get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM mahasiswa ORDER BY nim").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# READ ONE
def get_by_nim(nim):
    conn = get_connection()
    row = conn.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    return dict(row) if row else None


# CREATE
def create(nim, nama, program_studi, angkatan, ipk):
    conn = get_connection()
    conn.execute(
        "INSERT INTO mahasiswa (nim, nama, program_studi, angkatan, ipk) VALUES (?, ?, ?, ?, ?)",
        (nim, nama, program_studi, angkatan, ipk),
    )
    conn.commit()
    conn.close()


# UPDATE
def update(nim, nama, program_studi, angkatan, ipk):
    conn = get_connection()
    conn.execute(
        "UPDATE mahasiswa SET nama = ?, program_studi = ?, angkatan = ?, ipk = ? WHERE nim = ?",
        (nama, program_studi, angkatan, ipk, nim),
    )
    conn.commit()
    conn.close()


# DELETE
def delete(nim):
    conn = get_connection()
    conn.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
    conn.commit()
    conn.close()
