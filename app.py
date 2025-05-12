from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)

# Koneksi ke MySQL
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="simple_recipe"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bahan_input = [b.strip().lower() for b in request.form.getlist('bahan')]
        alat_input = [a.strip().lower() for a in request.form.getlist('alat')]

        cursor.execute("SELECT * FROM recipe")
        resep_list = cursor.fetchall()

        hasil = []

        for recipe in resep_list:
            id, nama, bahan_str, alat_str, langkah = recipe
            bahan_resep = [b.strip().lower() for b in bahan_str.split(',')]
            alat_resep = [a.strip().lower() for a in alat_str.split(',')]

            # Hitung kecocokan bahan
            bahan_cocok = sum(1 for b in bahan_resep if b in bahan_input)
            alat_cocok = sum(1 for a in alat_resep if a in alat_input)

            skor_bahan = bahan_cocok / len(bahan_resep) if bahan_resep else 0
            skor_alat = alat_cocok / len(alat_resep) if alat_resep else 0

            skor_total = round((skor_bahan + skor_alat) / 2 * 100, 2)  # dalam persen

            if skor_total > 0:  # Hanya tampilkan jika minimal ada yang cocok
                hasil.append({
                    'nama': nama,
                    'bahan': bahan_str,
                    'alat': alat_str,
                    'langkah': langkah,
                    'skor': skor_total
                })

        # Urutkan berdasarkan skor tertinggi
        hasil = sorted(hasil, key=lambda x: x['skor'], reverse=True)

        return render_template('hasil.html', hasil=hasil)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
