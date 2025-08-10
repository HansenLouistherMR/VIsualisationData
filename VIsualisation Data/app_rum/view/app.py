from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("Harap unggah file CSV atau TXT!", "danger")
            return redirect(url_for("index"))

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Jika file CSV → analisis data
        if filename.lower().endswith(".csv"):
            df = pd.read_csv(filepath)

            # Pastikan kolom sesuai
            expected_cols = ["inflasi", "suku_bunga", "cadangan_devisa", "transaksi"]
            for col in expected_cols:
                if col not in df.columns:
                    flash(f"Kolom '{col}' tidak ditemukan dalam file CSV!", "danger")
                    return redirect(url_for("index"))

            stats = df.describe().to_html(classes="table table-bordered")

            return render_template("result.html", 
                                   table=stats,
                                   filename=filename,
                                   type="csv")

        # Jika file TXT → tampilkan narasi
        elif filename.lower().endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            return render_template("result.html", 
                                   text_content=content,
                                   filename=filename,
                                   type="txt")

        else:
            flash("Format file tidak didukung! (Gunakan CSV atau TXT)", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
