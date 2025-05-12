Website rekomendasi masakan anak kost menggunakan sistem pakar

### Database MySql
```sql
CREATE DATABASE simple_recipe;

CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_resep VARCHAR(100),
    bahan TEXT,
    alat TEXT,
    langkah TEXT
);

```

### Langkah - langkah
1. Install package
```bash
pip install flask flask-mysqldb
```
3. run python
```bash
python app.py
```

