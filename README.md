# Granite-File-Analyzer
Granite File Analyzer is an interactive web application based on Streamlit for analyzing and interacting with various types of files (txt, py, csv, json, md, pdf, docx). This application also supports a chat feature with file content using an AI model based on LM Studio (Granite).

📂 Struktur Folder
Granite-File-Analyzer/
├── Granite_app.py
├── requirements.txt
├── README.md
└── png/
    ├── 1.png
    └── 2.png
    └── 3.png


⚡ Fitur Utama

Upload file: Mendukung berbagai format file seperti txt, py, csv, json, md, pdf, dan docx.

Ringkasan otomatis: Menyediakan informasi jumlah kata dan baris dalam file.

Analisis konten: Memberikan insights dan kesimpulan berdasarkan isi file.

Chat interaktif: Berinteraksi langsung dengan konten file menggunakan model AI ibm/granite-3.2-8b dari LM Studio.

History analisis: Menyimpan hingga 20 file terakhir yang dianalisis, dengan opsi untuk menghapus semua riwayat.

🛠 Instalasi & Jalankan Lokal

Clone repositori:

git clone https://github.com/Trisaputraezha/Granite-File-Analyzer.git
cd Granite-File-Analyzer


Install dependencies:

pip install -r requirements.txt


Isi requirements.txt:

streamlit
PyPDF2
python-docx
requests


Jalankan aplikasi:

streamlit run Granite_app.py


Akses aplikasi di browser pada:

http://localhost:8501

🔗 Konfigurasi LM Studio

URL LM Studio: Pastikan LM Studio berjalan dan dapat diakses pada URL berikut:

http://127.0.0.1:1234/v1


Model AI: Gunakan model ibm/granite-3.2-8b untuk analisis dan chat interaktif.

Output menjadi seperti ini :
## 📷 Screenshot Aplikasi

### 1️⃣ Tampilan Upload File
![Upload File](png/1.png)

### 2️⃣ Ringkasan & Judul File
![File Summary](png/2.png)

### 3️⃣ Chat Interaktif & Kesimpulan
![Chat Interactive](png/3.png)
