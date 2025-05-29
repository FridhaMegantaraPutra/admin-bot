# create_db.py

import sqlite3

data_makan = [
    (
        "I. PENYEDIAAN MAKAN SANTRI DAN GURU",
        """Pengurus akan mengelola penyediaan makan bagi santri dan guru kembali terhitung mulai tanggal 10 April 2025 dengan ketentuan sebagai berikut:

a. Biaya 3 kali makan sehari selama sebulan sebesar Rp. 540.000 (lima ratus empat puluh ribu rupiah);

b. Biaya 2 kali makan sehari (Senin–Sabtu) selama sebulan sebesar Rp. 450.000 (empat ratus lima puluh ribu rupiah);

c. Biaya 2 kali makan sehari (Senin–Sabtu) selama sebulan sebesar Rp. 300.000 (tiga ratus ribu rupiah).

Bagi santri yang tidak makan di pondok tidak diperkenankan melakukan kegiatan memasak sendiri secara pribadi ataupun berkelompok di dalam pondok.

Santri yang diketahui membawa alat masak ke dalam pondok akan diamankan oleh pengurus.

Pelunasan biaya makan dilakukan selambat-lambatnya tanggal 10 setiap bulannya, bersamaan dengan sodaqoh pondok."""
    )
]

def create_db():
    conn = sqlite3.connect("pondok.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS penyediaan_makan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        isi TEXT NOT NULL
    )
    """)

    cursor.execute("DELETE FROM penyediaan_makan")
    cursor.executemany("INSERT INTO penyediaan_makan (judul, isi) VALUES (?, ?)", data_makan)

    conn.commit()
    conn.close()
    print("✅ Database berhasil dibuat dan diisi.")

if __name__ == "__main__":
    create_db()
