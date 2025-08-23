# main.py
# Backend server untuk TrendLens yang sudah terintegrasi dengan scraper.

# Untuk menjalankan server ini:
# 1. Pastikan Anda sudah menginstal semua library dari scraper.py
#    (requests, beautifulsoup4, pytrends, pandas)
# 2. Install juga library untuk server: pip install fastapi uvicorn
# 3. Simpan file ini sebagai main.py dan scraper.py di folder yang sama.
# 4. Jalankan server dengan perintah: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import time

# --- Mengimpor fungsi scraper ---
# Pastikan file scraper.py berada di direktori yang sama.
from scraper import get_google_trends_score, get_shutterstock_competition

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="TrendLens API",
    description="API untuk menyediakan data tren microstock secara real-time.",
    version="1.1.0"
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Daftar Keyword untuk Dianalisis ---
# Di aplikasi nyata, daftar ini akan lebih dinamis, mungkin dari database
# atau berdasarkan input pengguna. Untuk MVP ini, kita tentukan di sini.
KEYWORDS_TO_ANALYZE = [
    "AI generated background",
    "sustainable lifestyle",
    "remote work setup",
    "mental health awareness",
    "local travel",
    "3d character",
    "cyber security"
]

# --- API Endpoints ---

@app.get("/")
def read_root():
    """Endpoint utama untuk mengecek status server."""
    return {"status": "TrendLens API (Integrated) is running!"}

@app.get("/api/v1/trends/analyze", response_model=List[Dict[str, Any]])
def get_analyzed_trends():
    """
    Endpoint utama yang melakukan analisis real-time.
    Ini akan memanggil scraper untuk setiap keyword dan mengembalikan hasilnya.
    """
    print("Menerima permintaan untuk analisis tren...")
    analyzed_data = []

    for i, keyword in enumerate(KEYWORDS_TO_ANALYZE):
        print(f"Menganalisis keyword ({i+1}/{len(KEYWORDS_TO_ANALYZE)}): '{keyword}'")

        # 1. Mengambil data permintaan (demand)
        demand_score = get_google_trends_score(keyword)
        
        # Jeda sesaat agar tidak membanjiri server
        time.sleep(1)

        # 2. Mengambil data kompetisi (supply)
        competition_count = get_shutterstock_competition(keyword)
        
        # 3. Menambahkan hasil ke daftar
        analyzed_data.append({
            "id": i + 1,
            "keyword": keyword,
            "demand_score": demand_score,
            "competition_count": competition_count,
        })
        
        # Jeda antar keyword
        time.sleep(1)

    # 4. (Opsional) Logika untuk memfilter hanya "Golden Keywords"
    # Di sini kita bisa menambahkan logika untuk menentukan mana yang terbaik.
    # Contoh: demand > 70 dan competition < 1,000,000
    golden_keywords = [
        item for item in analyzed_data 
        if item["demand_score"] > 60 and item["competition_count"] > 0 and item["competition_count"] < 5000000
    ]
    
    print("Analisis selesai. Mengirimkan hasil golden keywords.")
    return golden_keywords

# Komentar:
# Server ini sekarang sepenuhnya fungsional untuk MVP.
# Setiap kali frontend memanggil endpoint /api/v1/trends/analyze,
# server akan bekerja mengambil data terbaru dan mengirimkan hasilnya.
