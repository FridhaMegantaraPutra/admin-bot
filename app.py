import streamlit as st
import sqlite3
from groq import Groq
import os
from dotenv import load_dotenv
import docx

# Load API key dari file .env
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error("API Key tidak ditemukan di .env")
    st.stop()

client = Groq(api_key=API_KEY)

# Fungsi untuk memuat teks dari file .docx
def load_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# # Fungsi untuk mengambil data dari database SQLite
# def load_sql_data(db_path):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     # cursor.execute("SELECT nama_makhroj, deskripsi, contoh_huruf FROM makhroj")
#     cursor.execute("SELECT judul, isi FROM penyediaan_makan")

#     rows = cursor.fetchall()
#     conn.close()

#     hasil = []
#     for huruf, makhraj, ket in rows:
#         hasil.append(f"Huruf '{huruf}': keluar dari {makhraj}. Keterangan: {ket}")
#     return "\n".join(hasil)

# Fungsi untuk mengambil data dari database SQLite
def load_sql_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT judul, isi FROM penyediaan_makan")

    rows = cursor.fetchall()
    conn.close()

    hasil = []
    for judul, isi in rows:
        hasil.append(f"{judul}: {isi}")
    return "\n\n".join(hasil)


# Muat isi dari dokumen dan database
try:
    docx_text = load_docx("dokumen.docx")
    sql_text = load_sql_data("pondok.db")
    full_context = docx_text + "\n\n" + sql_text
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Chatbot Admin Pondok", layout="centered")
st.title("🗣️ ADMIN PPM BATU")
st.write("admin cerdas ready 24/7 libur hanya mitos anggaran 100% tidak terbuang dan saya suka memberi pelajaran pada santri ")

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input pengguna
if prompt := st.chat_input("Tanyakan tentang pondok pesantren batu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        try:
            # Prompt ketat agar hanya menjawab dari referensi
            system_prompt = (
                "Anda adalah asisten yang hanya boleh menjawab berdasarkan informasi berikut boleh dengan cara pharafrase dan friendly selagi tidak merubah konteks:\n\n"
                f"{full_context}\n\n"
                "Jika Anda tidak menemukan informasi dalam konteks ini, cukup jawab: "
                "'Maaf, pondok ini penuh rahasia akoakwokaowkoakwoak.'"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            # Lakukan streaming respons dari model
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stream=True,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                response_container.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungi API: {e}")
