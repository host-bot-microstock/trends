# scraper.py
# Modul untuk mengambil data dari Google Trends dan Shutterstock.

# Untuk menjalankan file ini dan menginstal library yang dibutuhkan:
# 1. Buka terminal atau command prompt.
# 2. Jalankan perintah berikut:
#    pip install requests beautifulsoup4 pytrends pandas

import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import pandas as pd
import time

# --- Fungsi untuk Mengukur Permintaan (Demand) ---

def get_google_trends_score(keyword: str) -> int:
    """
    Mengambil skor popularitas dari Google Trends untuk sebuah keyword.
    Mengembalikan nilai terakhir (paling baru) dari tren dalam rentang 0-100.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Membuat payload untuk query
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
        
        # Mengambil data interest over time
        interest_over_time_df = pytrends.interest_over_time()
        
        if interest_over_time_df.empty:
            print(f"Peringatan: Tidak ada data Google Trends untuk '{keyword}'.")
            return 0
            
        # Mengambil nilai tren terakhir (paling baru)
        last_score = interest_over_time_df[keyword].iloc[-1]
        
        print(f"Skor Google Trends untuk '{keyword}': {last_score}")
        return int(last_score)

    except Exception as e:
        print(f"Error saat mengambil data Google Trends untuk '{keyword}': {e}")
        # Jika ada error (misal: terlalu banyak request), kembalikan 0
        return 0

# --- Fungsi untuk Mengukur Kompetisi (Supply) ---

def get_shutterstock_competition(keyword: str) -> int:
    """
    Melakukan scraping ke Shutterstock untuk mengetahui jumlah aset (kompetisi).
    Mengembalikan jumlah total aset yang ditemukan untuk sebuah keyword.
    """
    # Mengganti spasi dengan '+' untuk URL
    formatted_keyword = keyword.replace(' ', '+')
    url = f"https://www.shutterstock.com/search/{formatted_keyword}"
    
    # Header dibutuhkan agar request terlihat seperti dari browser sungguhan
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Cek jika ada error HTTP
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari elemen yang berisi jumlah hasil.
        # Catatan: Class name ini bisa berubah. Perlu dicek secara berkala.
        # Selector ini mencari elemen yang cocok dengan pola class yang sering digunakan Shutterstock.
        result_element = soup.find('span', class_=lambda x: x and x.startswith('MuiTypography-root MuiTypography-body1'))

        if not result_element:
             # Fallback selector jika yang utama gagal
            result_element = soup.find('p', class_=lambda x: x and 'image' in x.lower())


        if result_element:
            # Membersihkan teks untuk mendapatkan angka saja
            # Contoh teks: "9,123,456 images"
            result_text = result_element.get_text(strip=True)
            # Mengambil angka dari teks
            number_str = ''.join(filter(str.isdigit, result_text))
            
            if number_str:
                competition_count = int(number_str)
                print(f"Jumlah kompetisi di Shutterstock untuk '{keyword}': {competition_count}")
                return competition_count

        print(f"Peringatan: Tidak dapat menemukan jumlah kompetisi untuk '{keyword}'.")
        return 0

    except requests.exceptions.RequestException as e:
        print(f"Error saat request ke Shutterstock untuk '{keyword}': {e}")
        return 0
    except Exception as e:
        print(f"Error saat parsing data Shutterstock untuk '{keyword}': {e}")
        return 0


# --- Blok untuk Testing ---
# Kode di bawah ini hanya akan berjalan jika Anda menjalankan file scraper.py secara langsung.
# Ini digunakan untuk memastikan fungsi-fungsi di atas bekerja dengan benar.
if __name__ == "__main__":
    test_keywords = ["AI generated background", "sustainable lifestyle", "zombie illustration"]
    
    print("--- Memulai Pengujian Scraper ---")
    for kw in test_keywords:
        print(f"\n--- Menganalisis Keyword: '{kw}' ---")
        
        # Mengambil skor demand
        demand = get_google_trends_score(kw)
        
        # Jeda sesaat agar tidak membanjiri server
        time.sleep(1) 
        
        # Mengambil skor supply
        competition = get_shutterstock_competition(kw)
        
        print("--- Hasil Analisis ---")
        print(f"Demand Score (Google Trends): {demand}")
        print(f"Competition (Shutterstock assets): {competition}")
        print("------------------------")
        
        time.sleep(2) # Jeda lebih lama antar keyword
