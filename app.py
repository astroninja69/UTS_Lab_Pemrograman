# app.py
from flask import Flask, redirect
from controllers.mahasiswa_controller import mahasiswa_bp
from models.mahasiswa_model import init_db

app = Flask(__name__)
app.register_blueprint(mahasiswa_bp)   # <- mendaftarkan semua route di mahasiswa_controller.py

init_db()   # <- buat tabel mahasiswa kalau belum ada


@app.route("/")
def home():
    return redirect("/mahasiswa")


if __name__ == "__main__":
    app.run(debug=True)
