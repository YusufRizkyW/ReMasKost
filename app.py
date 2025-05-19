from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Koneksi ke database baru: simple_recipe
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="simple_recipe"
)

cursor = conn.cursor()

def parse_item_with_weight(data_str):
    result = {}
    for item in data_str.split(','):
        parts = item.strip().lower().split(':')
        name = parts[0].strip()
        weight = int(parts[1]) if len(parts) > 1 else 1
        result[name] = weight
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bahan_input = [b.strip().lower() for b in request.form.getlist('bahan')]
        alat_input = [a.strip().lower() for a in request.form.getlist('alat')]

        cursor.execute("SELECT * FROM recipe")
        resep_list = cursor.fetchall()

        hasil = []

        for recipe in resep_list:
            id, nama_resep, bahan_str, alat_str, langkah = recipe

            bahan_resep = parse_item_with_weight(bahan_str)
            alat_resep = parse_item_with_weight(alat_str)

            total_bobot_bahan = sum(bahan_resep.values())
            total_bobot_alat = sum(alat_resep.values())

            bobot_bahan_cocok = sum(bobot for b, bobot in bahan_resep.items() if b in bahan_input)
            bobot_alat_cocok = sum(bobot for a, bobot in alat_resep.items() if a in alat_input)

            skor_bahan = bobot_bahan_cocok / total_bobot_bahan if total_bobot_bahan else 0
            skor_alat = bobot_alat_cocok / total_bobot_alat if total_bobot_alat else 0

            skor_total = round((0.7 * skor_bahan + 0.3 * skor_alat) * 100, 2)

            if skor_total > 0:
                hasil.append({
                    'judul': nama_resep,
                    'bahan': bahan_str,
                    'alat': alat_str,
                    'langkah': langkah,
                    'skor': skor_total
                })

        hasil = sorted(hasil, key=lambda x: x['skor'], reverse=True)
        return render_template('hasil.html', hasil=hasil)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
