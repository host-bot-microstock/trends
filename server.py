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
    # Teknologi & Masa Depan
    "AI generated background",
    "virtual reality experience",
    "metaverse avatar",
    "cyber security threat",
    "data visualization",
    "blockchain technology",
    "smart city",
    "robotics and automation",
    "quantum computing",
    "neural network",

    # Bisnis & Keuangan
    "remote work setup",
    "team collaboration online",
    "startup business meeting",
    "financial growth chart",
    "e-commerce shopping",
    "supply chain logistics",
    "digital marketing strategy",
    "customer service success",
    "real estate investment",
    "cryptocurrency trading",

    # Gaya Hidup & Kesejahteraan
    "sustainable lifestyle",
    "mental health awareness",
    "mindfulness and meditation",
    "work life balance",
    "healthy eating habits",
    "home workout",
    "digital detox",
    "local travel",
    "DIY home improvement",
    "pet adoption",

    # Alam & Lingkungan
    "climate change action",
    "renewable energy sources",
    "plastic pollution",
    "wildlife conservation",
    "drone aerial landscape",
    "forest bathing",
    "underwater photography",
    "extreme weather",
    "organic farming",
    "beautiful nature scenery",

    # Konsep Abstrak & Desain
    "retro futuristic",
    "abstract background",
    "geometric patterns",
    "liquid ink art",
    "3d render abstract",
    "minimalist design",
    "vaporwave aesthetic",
    "dark mode UI",
    "gradient mesh",
    "flat design illustration",

    # Orang & Keberagaman
    "diversity and inclusion",
    "multi-ethnic friends group",
    "empowered women",
    "senior couple enjoying retirement",
    "father and son bonding",
    "people with disabilities",
    "LGBTQ pride",
    "authentic portraits",
    "candid moments",
    "people working together",

    # Makanan & Minuman
    "plant-based food",
    "gourmet cooking",
    "artisanal coffee",
    "street food festival",
    "farm to table",
    "baking at home",
    "craft beer",
    "vegan recipe",
    "colorful cocktails",
    "healthy smoothie",

    # Perjalanan & Budaya
    "digital nomad lifestyle",
    "cultural festival",
    "adventure travel",
    "historical landmarks",
    "road trip",
    "eco tourism",
    "exotic destinations",
    "staycation",
    "world map",
    "traditional ceremony",

    # Pendidikan & Sains
    "online learning",
    "e-learning platform",
    "scientific research",
    "laboratory experiment",
    "back to school",
    "STEM education",
    "medical innovation",
    "DNA structure",
    "space exploration",
    "virtual classroom",

    # Musiman & Acara
    "new year celebration",
    "valentines day couple",
    "halloween spooky background",
    "christmas holiday season",
    "ramadan kareem",
    "black friday sale",
    "summer vacation",
    "autumn leaves",
    "winter wonderland",
    "spring flowers"
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
