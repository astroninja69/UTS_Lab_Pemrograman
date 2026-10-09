# controllers/mahasiswa_controller.py
from datetime import datetime
from flask import Blueprint, request, render_template, redirect
from models import mahasiswa_model

mahasiswa_bp = Blueprint("mahasiswa_bp", __name__)


def hitung_lama_studi(angkatan):
    # Lama Studi (tahun) = tahun sekarang - angkatan, dihitung oleh program
    return datetime.now().year - angkatan


def validasi(form, cek_nim=True):
    """Memeriksa input form. Mengembalikan (data, errors)."""
    errors = []
    data = {}

    nim = form.get("nim", "").strip()
    nama = form.get("nama", "").strip()
    program_studi = form.get("program_studi", "").strip()
    angkatan = form.get("angkatan", "").strip()
    ipk = form.get("ipk", "").strip().replace(",", ".")

    if cek_nim:
        if not nim:
            errors.append("NIM wajib diisi.")
        elif not nim.isdigit():
            errors.append("NIM harus berupa angka.")
        else:
            data["nim"] = int(nim)

    if not nama:
        errors.append("Nama wajib diisi.")
    data["nama"] = nama

    if not program_studi:
        errors.append("Program studi wajib diisi.")
    data["program_studi"] = program_studi

    if not angkatan:
        errors.append("Angkatan wajib diisi.")
    elif not angkatan.isdigit():
        errors.append("Angkatan harus berupa angka tahun, misalnya 2023.")
    else:
        data["angkatan"] = int(angkatan)

    if not ipk:
        errors.append("IPK wajib diisi.")
    else:
        try:
            nilai_ipk = float(ipk)
            if nilai_ipk < 0 or nilai_ipk > 4:      # nan juga ditolak di bawah
                errors.append("IPK harus di antara 0.00 sampai 4.00.")
            elif nilai_ipk != nilai_ipk:
                errors.append("IPK harus berupa angka, misalnya 3.50.")
            else:
                data["ipk"] = nilai_ipk
        except ValueError:
            errors.append("IPK harus berupa angka, misalnya 3.50.")

    return data, errors


# READ ALL  ->  GET /mahasiswa
@mahasiswa_bp.route("/mahasiswa", methods=["GET"])
def list_mahasiswa():
    daftar = mahasiswa_model.get_all()
    for m in daftar:
        m["lama_studi"] = hitung_lama_studi(m["angkatan"])
    return render_template("index.html", daftar=daftar)


# READ ONE  ->  GET /mahasiswa/123
@mahasiswa_bp.route("/mahasiswa/<int:nim>", methods=["GET"])
def detail_mahasiswa(nim):
    m = mahasiswa_model.get_by_nim(nim)
    if m is None:
        return "Mahasiswa tidak ditemukan!", 404
    m["lama_studi"] = hitung_lama_studi(m["angkatan"])
    return render_template("detail.html", m=m)


# FORM TAMBAH  ->  GET /mahasiswa/new
@mahasiswa_bp.route("/mahasiswa/new", methods=["GET"])
def show_form():
    return render_template("form.html", mode="tambah", m={}, errors=[])


# CREATE  ->  POST /mahasiswa/new
@mahasiswa_bp.route("/mahasiswa/new", methods=["POST"])
def submit_form():
    data, errors = validasi(request.form)

    # NIM harus unik: tolak kalau sudah terdaftar
    if "nim" in data and mahasiswa_model.get_by_nim(data["nim"]) is not None:
        errors.append("NIM " + str(data["nim"]) + " sudah terdaftar.")

    if errors:
        # tampilkan lagi form + pesan kesalahan, isian lama tidak hilang
        return render_template("form.html", mode="tambah", m=request.form, errors=errors), 400

    mahasiswa_model.create(data["nim"], data["nama"], data["program_studi"],
                           data["angkatan"], data["ipk"])
    return redirect("/mahasiswa")


# FORM EDIT  ->  GET /mahasiswa/123/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["GET"])
def show_edit_form(nim):
    m = mahasiswa_model.get_by_nim(nim)
    if m is None:
        return "Mahasiswa tidak ditemukan!", 404
    return render_template("form.html", mode="edit", m=m, errors=[])


# UPDATE  ->  POST /mahasiswa/123/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["POST"])
def update_mahasiswa(nim):
    if mahasiswa_model.get_by_nim(nim) is None:
        return "Mahasiswa tidak ditemukan!", 404

    # NIM tidak bisa diubah (sebagai identitas), jadi tidak perlu dicek lagi
    data, errors = validasi(request.form, cek_nim=False)

    if errors:
        isian = dict(request.form)
        isian["nim"] = nim
        return render_template("form.html", mode="edit", m=isian, errors=errors), 400

    mahasiswa_model.update(nim, data["nama"], data["program_studi"],
                           data["angkatan"], data["ipk"])
    return redirect("/mahasiswa")


# DELETE  ->  POST /mahasiswa/123/delete
@mahasiswa_bp.route("/mahasiswa/<int:nim>/delete", methods=["POST"])
def delete_mahasiswa(nim):
    if mahasiswa_model.get_by_nim(nim) is None:
        return "Mahasiswa tidak ditemukan!", 404
    mahasiswa_model.delete(nim)
    return redirect("/mahasiswa")
