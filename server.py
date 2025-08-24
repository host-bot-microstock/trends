# server.py (Versi Lengkap yang Sudah Diperbaiki)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import time

# --- Mengimpor fungsi scraper yang sudah diperbarui ---
# Pastikan file scraper.py berada di direktori yang sama.
from scraper import get_google_trends_score, get_shutterstock_competition_selenium

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="TrendLens API",
    description="API untuk menyediakan data tren microstock secara real-time.",
    version="1.2.0")  # Versi diperbarui

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Daftar Keyword untuk Dianalisis ---
# PENTING: Untuk testing awal, gunakan 5-10 keyword saja agar proses tidak terlalu lama dan tidak timeout.
# Hapus tanda komentar '#' pada daftar yang lebih pendek dan berikan tanda '#' pada daftar yang panjang.

# Daftar pendek untuk testing cepat
KEYWORDS_TO_ANALYZE = [
    "AI generated background",
    "sustainable lifestyle",
    "remote work setup",
    "mental health awareness",
    "cryptocurrency trading",
    "local travel",
    "plant-based food",
    "virtual reality experience",
    "diversity and inclusion",
    "retro futuristic",
]

# Daftar panjang (gunakan setelah yakin semuanya bekerja)
# KEYWORDS_TO_ANALYZE = [
#     "AI generated background", "virtual reality experience", "metaverse avatar", "cyber security threat",
#     "data visualization", "blockchain technology", "smart city", "robotics and automation",
#     "quantum computing", "neural network", "remote work setup", "team collaboration online",
#     "startup business meeting", "financial growth chart", "e-commerce shopping", "supply chain logistics",
#     "digital marketing strategy", "customer service success", "real estate investment", "cryptocurrency trading",
#     "sustainable lifestyle", "mental health awareness", "mindfulness and meditation", "work life balance",
#     "healthy eating habits", "home workout", "digital detox", "local travel", "DIY home improvement",
#     "pet adoption", "climate change action", "renewable energy sources", "plastic pollution",
#     "wildlife conservation", "drone aerial landscape", "forest bathing", "underwater photography",
#     "extreme weather", "organic farming", "beautiful nature scenery", "retro futuristic",
#     "abstract background", "geometric patterns", "liquid ink art", "3d render abstract",
#     "minimalist design", "vaporwave aesthetic", "dark mode UI", "gradient mesh", "flat design illustration",
#     "diversity and inclusion", "multi-ethnic friends group", "empowered women",
#     "senior couple enjoying retirement", "father and son bonding", "people with disabilities", "LGBTQ pride",
#     "authentic portraits", "candid moments", "people working together", "plant-based food", "gourmet cooking",
#     "artisanal coffee", "street food festival", "farm to table", "baking at home", "craft beer",
#     "vegan recipe", "colorful cocktails", "healthy smoothie", "digital nomad lifestyle",
#     "cultural festival", "adventure travel", "historical landmarks", "road trip", "eco tourism",
#     "exotic destinations", "staycation", "world map", "traditional ceremony", "online learning",
#     "e-learning platform", "scientific research", "laboratory experiment", "back to school",
#     "STEM education", "medical innovation", "DNA structure", "space exploration", "virtual classroom",
#     "new year celebration", "valentines day couple", "halloween spooky background",
#     "christmas holiday season", "ramadan kareem", "black friday sale", "summer vacation",
#     "autumn leaves", "winter wonderland", "spring flowers"
# ]


# --- API Endpoints ---
@app.get("/")
def read_root():
    """Endpoint utama untuk mengecek status server."""
    return {"status": "TrendLens API (Selenium Integrated) is running!"}


@app.get("/api/v1/trends/analyze", response_model=List[Dict[str, Any]])
def get_analyzed_trends():
    """
    Endpoint utama yang melakukan analisis real-time menggunakan scraper yang telah diperbarui.
    """
    print("Menerima permintaan untuk analisis tren...")
    analyzed_data = []
    total_keywords = len(KEYWORDS_TO_ANALYZE)

    for i, keyword in enumerate(KEYWORDS_TO_ANALYZE):
        print(
            f"\n---> Menganalisis keyword ({i+1}/{total_keywords}): '{keyword}' <---"
        )

        # 1. Mengambil data permintaan (demand)
        demand_score = get_google_trends_score(keyword)

        # 2. Mengambil data kompetisi (supply) dengan Selenium
        competition_count = get_shutterstock_competition_selenium(keyword)

        # 3. Menambahkan hasil ke daftar
        if demand_score > 0 or competition_count > 0:  # Hanya tambahkan jika ada data
            analyzed_data.append({
                "id": i + 1,
                "keyword": keyword,
                "demand_score": demand_score,
                "competition_count": competition_count,
            })
        else:
            print(
                f"Melewatkan keyword '{keyword}' karena tidak ada data demand atau kompetisi."
            )

    print("\nAnalisis selesai. Mengirimkan hasil.")
    return analyzed_data
