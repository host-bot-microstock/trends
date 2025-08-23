# scraper.py
# Versi perbaikan dengan anti-blocking dan tambahan Adobe Stock.

import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import pandas as pd
import time
import random

# --- Fungsi untuk Mengukur Permintaan (Demand) ---

def get_google_trends_score(keyword: str) -> int:
    """
    Mengambil skor popularitas dari Google Trends untuk sebuah keyword.
    """
    try:
        time.sleep(random.uniform(2, 5))
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
        interest_over_time_df = pytrends.interest_over_time()
        
        if interest_over_time_df.empty:
            print(f"Peringatan: Tidak ada data Google Trends untuk '{keyword}'.")
            return 0
            
        last_score = interest_over_time_df[keyword].iloc[-1]
        print(f"Skor Google Trends untuk '{keyword}': {last_score}")
        return int(last_score)

    except Exception as e:
        print(f"Error saat mengambil data Google Trends untuk '{keyword}': {e}")
        return 0

# --- Fungsi untuk Mengukur Kompetisi (Supply) ---

def get_shutterstock_competition(keyword: str) -> int:
    """
    Melakukan scraping ke Shutterstock untuk mengetahui jumlah aset (kompetisi).
    """
    time.sleep(random.uniform(1, 4))
    formatted_keyword = keyword.replace(' ', '+')
    url = f"https://www.shutterstock.com/search/{formatted_keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        result_element = soup.find('span', class_=lambda x: x and x.startswith('MuiTypography-root MuiTypography-body1'))

        if result_element:
            result_text = result_element.get_text(strip=True)
            number_str = ''.join(filter(str.isdigit, result_text))
            if number_str:
                competition_count = int(number_str)
                print(f"Jumlah kompetisi di Shutterstock untuk '{keyword}': {competition_count}")
                return competition_count

        print(f"Peringatan: Tidak dapat menemukan jumlah kompetisi Shutterstock untuk '{keyword}'.")
        return 0
    except Exception as e:
        print(f"Error saat request ke Shutterstock untuk '{keyword}': {e}")
        return 0

def get_adobe_stock_competition(keyword: str) -> int:
    """
    Melakukan scraping ke Adobe Stock untuk mengetahui jumlah aset (kompetisi).
    """
    time.sleep(random.uniform(1, 4))
    formatted_keyword = keyword.replace(' ', '+')
    url = f"https://stock.adobe.com/search?k={formatted_keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Adobe Stock menggunakan class 'nb-results' untuk menampilkan jumlah
        result_element = soup.find('span', class_='nb-results')

        if result_element:
            result_text = result_element.get_text(strip=True)
            # Teksnya bisa "12,345 Results" atau "12.345 Ergebnisse" tergantung bahasa
            number_str = ''.join(filter(str.isdigit, result_text))
            if number_str:
                competition_count = int(number_str)
                print(f"Jumlah kompetisi di Adobe Stock untuk '{keyword}': {competition_count}")
                return competition_count

        print(f"Peringatan: Tidak dapat menemukan jumlah kompetisi Adobe Stock untuk '{keyword}'.")
        return 0
    except Exception as e:
        print(f"Error saat request ke Adobe Stock untuk '{keyword}': {e}")
        return 0


# --- Blok untuk Testing ---
if __name__ == "__main__":
    test_keywords = ["AI generated background", "sustainable lifestyle"]
    
    print("--- Memulai Pengujian Scraper ---")
    for kw in test_keywords:
        print(f"\n--- Menganalisis Keyword: '{kw}' ---")
        
        demand = get_google_trends_score(kw)
        shutterstock_comp = get_shutterstock_competition(kw)
        adobe_stock_comp = get_adobe_stock_competition(kw)
        
        print("--- Hasil Analisis ---")
        print(f"Demand Score (Google Trends): {demand}")
        print(f"Shutterstock Competition: {shutterstock_comp}")
        print(f"Adobe Stock Competition: {adobe_stock_comp}")
        print("------------------------")
